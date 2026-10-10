"""Install converter outputs together, restoring old files after I/O failures.

Generation and validation finish before any destination files are changed.
This is rollback for ordinary process errors, not power-loss atomicity or a
transaction against other processes writing the same files concurrently.
"""
from contextlib import contextmanager
import io
import os
from pathlib import Path
import shutil
import sys
import tempfile


class OutputBundle:
    def __init__(self):
        self.files = {}

    @contextmanager
    def open(self, filename, mode='w', encoding='utf-8'):
        """Buffer a complete output; a failed writer does not register it."""
        path = Path(os.path.abspath(filename))
        if path in self.files:
            raise ValueError(f'Duplicate output destination: {path}')
        if mode not in ('w', 'wb'):
            raise ValueError('OutputBundle supports only w and wb')
        with (io.BytesIO() if mode == 'wb' else io.StringIO()) as output:
            yield output
            data = output.getvalue()
            self.files[path] = data if mode == 'wb' else data.encode(encoding)

    @staticmethod
    def _temporary(path, kind):
        fd, filename = tempfile.mkstemp(prefix=f'.hutrack-{kind}-', suffix='-'+path.name,
                                        dir=path.parent)
        os.close(fd)
        return Path(filename)

    def commit(self):
        # Check every target before making directories, stages or backups.
        for path in self.files:
            if path.is_symlink() or (path.exists() and not path.is_file()):
                raise ValueError(f'Output destination must be a regular file: {path}')
            for parent in path.parents:
                if parent in self.files or (parent.exists() and not parent.is_dir()):
                    raise ValueError(f'Output parent must be a directory: {parent}')

        stages, backups, installed, created_dirs = {}, {}, [], []
        keep_backups = False
        try:
            for path, data in self.files.items():
                missing = []
                parent = path.parent
                while not parent.exists():
                    missing.append(parent)
                    parent = parent.parent
                for directory in reversed(missing):
                    directory.mkdir()
                    created_dirs.append(directory)
                stage = self._temporary(path, 'stage')
                stages[path] = stage
                with stage.open('wb') as output:
                    output.write(data)

            # Keep originals in place until every stage and backup is ready.
            for path in self.files:
                if path.exists():
                    backup = self._temporary(path, 'backup')
                    backups[path] = backup
                    # Keep backups writable even if an original is read-only;
                    # failed installation must still be able to clean up.
                    shutil.copyfile(path, backup)
            for path, stage in stages.items():
                os.replace(stage, path)
                installed.append(path)
        except BaseException as error:
            rollback_errors = []
            for path in reversed(installed):
                try:
                    if path in backups:
                        os.replace(backups[path], path)
                    else:
                        path.unlink()
                except OSError as restore_error:
                    rollback_errors.append(f'{path}: {restore_error}')
            if rollback_errors:
                # Never erase the only remaining copy after a restore failure.
                keep_backups = True
                locations = ', '.join(str(p) for p in backups.values() if p.exists())
                raise OSError('Output rollback failed: ' + '; '.join(rollback_errors)
                              + '. Recovery backups: ' + locations) from error
            raise
        finally:
            for temporary in list(stages.values()) + ([] if keep_backups else list(backups.values())):
                try:
                    temporary.unlink(missing_ok=True)
                except OSError as cleanup_error:
                    # Cleanup does not change whether installation succeeded,
                    # and must never mask an installation/rollback error.
                    print(f'Warning: cannot remove temporary output {temporary}: {cleanup_error}',
                          file=sys.stderr)
            for directory in reversed(created_dirs):
                try:
                    directory.rmdir()  # Only remove empty directories we created.
                except OSError:
                    pass

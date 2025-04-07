
.data.chan5


;..........................
; frame 0

  .db $aa, $0                                   ; Pattern Index # 0
  .db $ab, $2                                   ; Pattern # 2
  .db $5f                                       ; 804 -> $5f
  .db $1f                                       ; 804 -> $1f
  .db $b0, $0                                   ; Waveform update #$0
  .db $a5, $ff                                  ; 805 -> $ff
  .db $a8, $ff                                  ; 808 -> $ff
  .db $a9, $0                                   ; 809 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 1

  .db $ff                                       ; Wait vblank

;..........................
; frame 2

  .db $ff                                       ; Wait vblank

;..........................
; frame 3

  .db $ff                                       ; Wait vblank

;..........................
; frame 4

  .db $ff                                       ; Wait vblank

;..........................
; frame 5

  .db $ff                                       ; Wait vblank

;..........................
; frame 6

  .db $ff                                       ; Wait vblank

;..........................
; frame 7

  .db $ff                                       ; Wait vblank

;..........................
; frame 8

  .db $ff                                       ; Wait vblank

;..........................
; frame 9

  .db $ff                                       ; Wait vblank

;..........................
; frame 10

  .db $ff                                       ; Wait vblank

;..........................
; frame 11

  .db $ff                                       ; Wait vblank

;..........................
; frame 12

  .db $ff                                       ; Wait vblank

;..........................
; frame 13

  .db $ff                                       ; Wait vblank

;..........................
; frame 14

  .db $ff                                       ; Wait vblank

;..........................
; frame 15

  .db $ff                                       ; Wait vblank

;..........................
; frame 16

  .db $9d                                       ; 804 -> $9d
  .db $99                                       ; 804 -> $99
  .db $5f                                       ; 804 -> $5f
  .db $1f                                       ; 804 -> $1f
  .db $b0, $3                                   ; Waveform update #$3
  .db $99                                       ; 804 -> $99
  .db $c1, $53                                  ; 802 -> $1, 803 -> $53
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 17

  .db $9d                                       ; 804 -> $9d
  .db $c0, $aa                                  ; 802 -> $0, 803 -> $aa
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 18

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 19

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 20

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 21

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 22

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 23

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 24

  .db $9d                                       ; 804 -> $9d
  .db $98                                       ; 804 -> $98
  .db $c0, $aa                                  ; 802 -> $0, 803 -> $aa
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 25

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 26

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 27

  .db $92                                       ; 804 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 28

  .db $90                                       ; 804 -> $90
  .db $ff                                       ; Wait vblank

;..........................
; frame 29

  .db $8e                                       ; 804 -> $8e
  .db $ff                                       ; Wait vblank

;..........................
; frame 30

  .db $8d                                       ; 804 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 31

  .db $8b                                       ; 804 -> $8b
  .db $ff                                       ; Wait vblank

;..........................
; frame 32

  .db $89                                       ; 804 -> $89
  .db $ff                                       ; Wait vblank

;..........................
; frame 33

  .db $87                                       ; 804 -> $87
  .db $ff                                       ; Wait vblank

;..........................
; frame 34

  .db $85                                       ; 804 -> $85
  .db $ff                                       ; Wait vblank

;..........................
; frame 35

  .db $83                                       ; 804 -> $83
  .db $ff                                       ; Wait vblank

;..........................
; frame 36

  .db $81                                       ; 804 -> $81
  .db $ff                                       ; Wait vblank

;..........................
; frame 37

  .db $80                                       ; 804 -> $80
  .db $ff                                       ; Wait vblank

;..........................
; frame 38

  .db $80                                       ; 804 -> $80
  .db $ff                                       ; Wait vblank

;..........................
; frame 39

  .db $80                                       ; 804 -> $80
  .db $ff                                       ; Wait vblank

;..........................
; frame 40

  .db $9d                                       ; 804 -> $9d
  .db $99                                       ; 804 -> $99
  .db $c1, $68                                  ; 802 -> $1, 803 -> $68
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 41

  .db $9d                                       ; 804 -> $9d
  .db $c0, $b4                                  ; 802 -> $0, 803 -> $b4
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 42

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 43

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 44

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 45

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 46

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 47

  .db $fd                                       ; Stop sample
  .db $c0, $b4                                  ; 802 -> $0, 803 -> $b4
  .db $a7, $0                                   ; 807 -> $0
  .db $0                                        ; 804 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 48

  .db $9d                                       ; 804 -> $9d
  .db $99                                       ; 804 -> $99
  .db $c1, $53                                  ; 802 -> $1, 803 -> $53
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 49

  .db $9d                                       ; 804 -> $9d
  .db $c0, $aa                                  ; 802 -> $0, 803 -> $aa
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 50

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 51

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 52

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 53

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 54

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 55

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 56

  .db $98                                       ; 804 -> $98
  .db $ff                                       ; Wait vblank

;..........................
; frame 57

  .db $98                                       ; 804 -> $98
  .db $ff                                       ; Wait vblank

;..........................
; frame 58

  .db $98                                       ; 804 -> $98
  .db $ff                                       ; Wait vblank

;..........................
; frame 59

  .db $97                                       ; 804 -> $97
  .db $ff                                       ; Wait vblank

;..........................
; frame 60

  .db $97                                       ; 804 -> $97
  .db $ff                                       ; Wait vblank

;..........................
; frame 61

  .db $97                                       ; 804 -> $97
  .db $ff                                       ; Wait vblank

;..........................
; frame 62

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 63

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 64

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 65

  .db $95                                       ; 804 -> $95
  .db $ff                                       ; Wait vblank

;..........................
; frame 66

  .db $95                                       ; 804 -> $95
  .db $ff                                       ; Wait vblank

;..........................
; frame 67

  .db $95                                       ; 804 -> $95
  .db $ff                                       ; Wait vblank

;..........................
; frame 68

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 69

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 70

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 71

  .db $93                                       ; 804 -> $93
  .db $ff                                       ; Wait vblank

;..........................
; frame 72

  .db $98                                       ; 804 -> $98
  .db $94                                       ; 804 -> $94
  .db $c0, $aa                                  ; 802 -> $0, 803 -> $aa
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 73

  .db $92                                       ; 804 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 74

  .db $91                                       ; 804 -> $91
  .db $ff                                       ; Wait vblank

;..........................
; frame 75

  .db $8f                                       ; 804 -> $8f
  .db $ff                                       ; Wait vblank

;..........................
; frame 76

  .db $8d                                       ; 804 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 77

  .db $8c                                       ; 804 -> $8c
  .db $ff                                       ; Wait vblank

;..........................
; frame 78

  .db $8a                                       ; 804 -> $8a
  .db $ff                                       ; Wait vblank

;..........................
; frame 79

  .db $89                                       ; 804 -> $89
  .db $ff                                       ; Wait vblank

;..........................
; frame 80

  .db $87                                       ; 804 -> $87
  .db $ff                                       ; Wait vblank

;..........................
; frame 81

  .db $86                                       ; 804 -> $86
  .db $ff                                       ; Wait vblank

;..........................
; frame 82

  .db $84                                       ; 804 -> $84
  .db $ff                                       ; Wait vblank

;..........................
; frame 83

  .db $83                                       ; 804 -> $83
  .db $ff                                       ; Wait vblank

;..........................
; frame 84

  .db $81                                       ; 804 -> $81
  .db $ff                                       ; Wait vblank

;..........................
; frame 85

  .db $80                                       ; 804 -> $80
  .db $ff                                       ; Wait vblank

;..........................
; frame 86

  .db $80                                       ; 804 -> $80
  .db $ff                                       ; Wait vblank

;..........................
; frame 87

  .db $80                                       ; 804 -> $80
  .db $ff                                       ; Wait vblank

;..........................
; frame 88

  .db $9d                                       ; 804 -> $9d
  .db $99                                       ; 804 -> $99
  .db $c1, $68                                  ; 802 -> $1, 803 -> $68
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 89

  .db $9d                                       ; 804 -> $9d
  .db $c0, $b4                                  ; 802 -> $0, 803 -> $b4
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 90

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 91

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 92

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 93

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 94

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 95

  .db $c0, $b4                                  ; 802 -> $0, 803 -> $b4
  .db $a7, $0                                   ; 807 -> $0
  .db $0                                        ; 804 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 96

  .db $9d                                       ; 804 -> $9d
  .db $99                                       ; 804 -> $99
  .db $c1, $53                                  ; 802 -> $1, 803 -> $53
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 97

  .db $9d                                       ; 804 -> $9d
  .db $c0, $aa                                  ; 802 -> $0, 803 -> $aa
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 98

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 99

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 100

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 101

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 102

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 103

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 104

  .db $98                                       ; 804 -> $98
  .db $ff                                       ; Wait vblank

;..........................
; frame 105

  .db $98                                       ; 804 -> $98
  .db $ff                                       ; Wait vblank

;..........................
; frame 106

  .db $98                                       ; 804 -> $98
  .db $ff                                       ; Wait vblank

;..........................
; frame 107

  .db $97                                       ; 804 -> $97
  .db $ff                                       ; Wait vblank

;..........................
; frame 108

  .db $97                                       ; 804 -> $97
  .db $ff                                       ; Wait vblank

;..........................
; frame 109

  .db $97                                       ; 804 -> $97
  .db $ff                                       ; Wait vblank

;..........................
; frame 110

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 111

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 112

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 113

  .db $95                                       ; 804 -> $95
  .db $ff                                       ; Wait vblank

;..........................
; frame 114

  .db $95                                       ; 804 -> $95
  .db $ff                                       ; Wait vblank

;..........................
; frame 115

  .db $95                                       ; 804 -> $95
  .db $ff                                       ; Wait vblank

;..........................
; frame 116

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 117

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 118

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 119

  .db $c0, $aa                                  ; 802 -> $0, 803 -> $aa
  .db $a7, $0                                   ; 807 -> $0
  .db $0                                        ; 804 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 120

  .db $9d                                       ; 804 -> $9d
  .db $99                                       ; 804 -> $99
  .db $c1, $fc                                  ; 802 -> $1, 803 -> $fc
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 121

  .db $9d                                       ; 804 -> $9d
  .db $c0, $fe                                  ; 802 -> $0, 803 -> $fe
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 122

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 123

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 124

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 125

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 126

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 127

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 128

  .db $9d                                       ; 804 -> $9d
  .db $98                                       ; 804 -> $98
  .db $c0, $fe                                  ; 802 -> $0, 803 -> $fe
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 129

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 130

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 131

  .db $92                                       ; 804 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 132

  .db $90                                       ; 804 -> $90
  .db $ff                                       ; Wait vblank

;..........................
; frame 133

  .db $8e                                       ; 804 -> $8e
  .db $ff                                       ; Wait vblank

;..........................
; frame 134

  .db $8d                                       ; 804 -> $8d
  .db $ff                                       ; Wait vblank

;..........................
; frame 135

  .db $c0, $fe                                  ; 802 -> $0, 803 -> $fe
  .db $a7, $0                                   ; 807 -> $0
  .db $0                                        ; 804 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 136

  .db $9d                                       ; 804 -> $9d
  .db $99                                       ; 804 -> $99
  .db $c1, $ac                                  ; 802 -> $1, 803 -> $ac
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 137

  .db $9d                                       ; 804 -> $9d
  .db $c0, $d6                                  ; 802 -> $0, 803 -> $d6
  .db $a7, $0                                   ; 807 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 138

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 139

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 140

  .db $9a                                       ; 804 -> $9a
  .db $ff                                       ; Wait vblank

;..........................
; frame 141

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 142

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 143

  .db $99                                       ; 804 -> $99
  .db $ff                                       ; Wait vblank

;..........................
; frame 144

  .db $98                                       ; 804 -> $98
  .db $ff                                       ; Wait vblank

;..........................
; frame 145

  .db $98                                       ; 804 -> $98
  .db $ff                                       ; Wait vblank

;..........................
; frame 146

  .db $98                                       ; 804 -> $98
  .db $ff                                       ; Wait vblank

;..........................
; frame 147

  .db $97                                       ; 804 -> $97
  .db $ff                                       ; Wait vblank

;..........................
; frame 148

  .db $97                                       ; 804 -> $97
  .db $ff                                       ; Wait vblank

;..........................
; frame 149

  .db $97                                       ; 804 -> $97
  .db $ff                                       ; Wait vblank

;..........................
; frame 150

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 151

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 152

  .db $96                                       ; 804 -> $96
  .db $ff                                       ; Wait vblank

;..........................
; frame 153

  .db $95                                       ; 804 -> $95
  .db $ff                                       ; Wait vblank

;..........................
; frame 154

  .db $95                                       ; 804 -> $95
  .db $ff                                       ; Wait vblank

;..........................
; frame 155

  .db $95                                       ; 804 -> $95
  .db $ff                                       ; Wait vblank

;..........................
; frame 156

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 157

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 158

  .db $94                                       ; 804 -> $94
  .db $ff                                       ; Wait vblank

;..........................
; frame 159

  .db $93                                       ; 804 -> $93
  .db $ff                                       ; Wait vblank

;..........................
; frame 160

  .db $93                                       ; 804 -> $93
  .db $ff                                       ; Wait vblank

;..........................
; frame 161

  .db $93                                       ; 804 -> $93
  .db $ff                                       ; Wait vblank

;..........................
; frame 162

  .db $92                                       ; 804 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 163

  .db $92                                       ; 804 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 164

  .db $92                                       ; 804 -> $92
  .db $ff                                       ; Wait vblank

;..........................
; frame 165

  .db $91                                       ; 804 -> $91
  .db $ff                                       ; Wait vblank

;..........................
; frame 166

  .db $91                                       ; 804 -> $91
  .db $ff                                       ; Wait vblank

;..........................
; frame 167

  .db $91                                       ; 804 -> $91
  .db $ff                                       ; Wait vblank

;..........................
; frame 168

  .db $c0, $d6                                  ; 802 -> $0, 803 -> $d6
  .db $a7, $0                                   ; 807 -> $0
  .db $0                                        ; 804 -> $0
  .db $ff                                       ; Wait vblank

;..........................
; frame 169

  .db $ff                                       ; Wait vblank

;..........................
; frame 170

  .db $ff                                       ; Wait vblank

;..........................
; frame 171

  .db $ff                                       ; Wait vblank

;..........................
; frame 172

  .db $ff                                       ; Wait vblank

;..........................
; frame 173

  .db $ff                                       ; Wait vblank

;..........................
; frame 174

  .db $ff                                       ; Wait vblank

;..........................
; frame 175

  .db $ff                                       ; Wait vblank

;..........................
; frame 176

  .db $ff                                       ; Wait vblank

;..........................
; frame 177

  .db $ff                                       ; Wait vblank

;..........................
; frame 178

  .db $ff                                       ; Wait vblank

;..........................
; frame 179

  .db $ff                                       ; Wait vblank

;..........................
; frame 180

  .db $ff                                       ; Wait vblank

;..........................
; frame 181

  .db $ff                                       ; Wait vblank

;..........................
; frame 182

  .db $ff                                       ; Wait vblank

;..........................
; frame 183

  .db $ff                                       ; Wait vblank

;..........................
; frame 184

  .db $ff                                       ; Wait vblank

;..........................
; frame 185

  .db $ff                                       ; Wait vblank

;..........................
; frame 186

  .db $ff                                       ; Wait vblank

;..........................
; frame 187

  .db $ff                                       ; Wait vblank

;..........................
; frame 188

  .db $ff                                       ; Wait vblank

;..........................
; frame 189

  .db $ff                                       ; Wait vblank

;..........................
; frame 190

  .db $ff                                       ; Wait vblank

;..........................
; frame 191

  .db $ff                                       ; Wait vblank

;..........................
; frame 192

  .db $ff                                       ; Wait vblank

;..........................
; frame 193

  .db $fb                                       ; End of channel stream
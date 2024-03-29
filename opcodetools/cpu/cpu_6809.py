import opcodetools.cpu.base_cpu
from opcodetools.cpu.base_assembly import AssemblyException
from opcodetools.cpu.opcode import Opcode

# The "yy" fill-in indicates one of the possible post codes.
# Opcodes have at most one fill-in value.
# The fill-in can be at the end or in the middle -- never at the beginning.

OPCODES = [

    {"mnemonic": "LDY #w",           "code": "108Ew1w0",         "use": "w=const"      },
    {"mnemonic": "NEG p",            "code": "00pp",             "use": "p=data_bp_rw" },
    {"mnemonic": "COM p",            "code": "03pp",             "use": "p=data_bp_rw" },
    {"mnemonic": "LSR p",            "code": "04pp",             "use": "p=data_bp_rw" },
    {"mnemonic": "ROR p",            "code": "06pp",             "use": "p=data_bp_rw" },
    {"mnemonic": "ASR p",            "code": "07pp",             "use": "p=data_bp_rw" },
    {"mnemonic": "LSL p",            "code": "08pp",             "use": "p=data_bp_rw" },
    {"mnemonic": "ASL p",            "code": "08pp",             "use": "p=data_bp_rw" },
    {"mnemonic": "ROL p",            "code": "09pp",             "use": "p=data_bp_rw" },
    {"mnemonic": "DEC p",            "code": "0App",             "use": "p=data_bp_rw" },
    {"mnemonic": "INC p",            "code": "0Cpp",             "use": "p=data_bp_rw" },
    {"mnemonic": "TST p",            "code": "0Dpp",             "use": "p=data_bp_r"  },
    {"mnemonic": "JMP p",            "code": "0Epp",             "use": "p=code_bp"    },
    {"mnemonic": "CLR p",            "code": "0Fpp",             "use": "p=data_bp_w"  },
    {"mnemonic": "LBRN s",           "code": "1021s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBHI s",           "code": "1022s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBLS s",           "code": "1023s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBHS s",           "code": "1024s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBCC s",           "code": "1024s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBCS s",           "code": "1025s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBLO s",           "code": "1025s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBNE s",           "code": "1026s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBEQ s",           "code": "1027s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBVC s",           "code": "1028s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBVS s",           "code": "1029s1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBPL s",           "code": "102As1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBMI s",           "code": "102Bs1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBGE s",           "code": "102Cs1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBLT s",           "code": "102Ds1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBGT s",           "code": "102Es1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "LBLE s",           "code": "102Fs1s0",         "use": "s=code_pcr"   },
    {"mnemonic": "SWI2",             "code": "103F",             "use": ""             },
    {"mnemonic": "CMPD #w",          "code": "1083w1w0",         "use": "w=const"      },
    {"mnemonic": "CMPY #w",          "code": "108Cw1w0",         "use": "w=const"      },
    {"mnemonic": "CMPD p",           "code": "1093pp",           "use": "p=data_bp_r"  },
    {"mnemonic": "CMPY p",           "code": "109Cpp",           "use": "p=data_bp_r"  },
    {"mnemonic": "LDY p",            "code": "109Epp",           "use": "p=data_bp_r"  },
    {"mnemonic": "STY p",            "code": "109Fpp",           "use": "p=data_bp_w"  },
    {"mnemonic": "CMPD y",           "code": "10A3yy",           "use": "y_r"          },
    {"mnemonic": "CMPY y",           "code": "10ACyy",           "use": "y_r"          },
    {"mnemonic": "LDY y",            "code": "10AEyy",           "use": "y_r"          },
    {"mnemonic": "STY y",            "code": "10AFyy",           "use": "y_w"          },
    {"mnemonic": "CMPD t",           "code": "10B3t1t0",         "use": "t=data_r"     },
    {"mnemonic": "CMPY t",           "code": "10BCt1t0",         "use": "t=data_r"     },
    {"mnemonic": "LDY t",            "code": "10BEt1t0",         "use": "t=data_r"     },
    {"mnemonic": "STY t",            "code": "10BFt1t0",         "use": "t=data_w"     },
    {"mnemonic": "LDS #w",           "code": "10CEw1w0",         "use": "w=const"      },
    {"mnemonic": "LDS p",            "code": "10DEpp",           "use": "p=data_bp_r"  },
    {"mnemonic": "STS p",            "code": "10DFpp",           "use": "p=data_bp_w"  },
    {"mnemonic": "LDS y",            "code": "10EEyy",           "use": "y_r"          },
    {"mnemonic": "STS y",            "code": "10EFyy",           "use": "y_w"          },
    {"mnemonic": "LDS t",            "code": "10FEt1t0",         "use": "t=data_r"     },
    {"mnemonic": "STS t",            "code": "10FFt1t0",         "use": "t=data_w"     },
    {"mnemonic": "SWI3",             "code": "113F",             "use": ""             },
    {"mnemonic": "CMPU #w",          "code": "1183w1w0",         "use": "w=const"      },
    {"mnemonic": "CMPS #w",          "code": "118Cw1w0",         "use": "w=const"      },
    {"mnemonic": "CMPU p",           "code": "1193pp",           "use": "p=data_bp_r"  },
    {"mnemonic": "CMPS p",           "code": "119Cpp",           "use": "p=data_bp_r"  },
    {"mnemonic": "CMPU y",           "code": "11A3yy",           "use": "y_r"          },
    {"mnemonic": "CMPS y",           "code": "11ACyy",           "use": "y_r"          },
    {"mnemonic": "CMPU t",           "code": "11B3t1t0",         "use": "t=data_r"     },
    {"mnemonic": "CMPS t",           "code": "11BCt1t0",         "use": "t=data_r"     },
    {"mnemonic": "NOP",              "code": "12",               "use": ""             },
    {"mnemonic": "SYNC",             "code": "13",               "use": ""             },
    {"mnemonic": "LBRA s",           "code": "16s1s0",           "use": "s=code_pcr"   },
    {"mnemonic": "LBSR s",           "code": "17s1s0",           "use": "s=code_pcr"   },
    {"mnemonic": "DAA",              "code": "19",               "use": ""             },
    {"mnemonic": "ORCC #b",          "code": "1Abb",             "use": "b=const"      },
    {"mnemonic": "ANDCC #b",         "code": "1Cbb",             "use": "b=const"      },
    {"mnemonic": "SEX",              "code": "1D",               "use": ""             },
    {"mnemonic": "EXG z",            "code": "1Ezz",             "use": "z=const_pair" },
    {"mnemonic": "TFR z",            "code": "1Fzz",             "use": "z=const_pair" },
    {"mnemonic": "BRA r",            "code": "20rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BRN r",            "code": "21rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BHI r",            "code": "22rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BLS r",            "code": "23rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BHS r",            "code": "24rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BCC r",            "code": "24rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BCS r",            "code": "25rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BLO r",            "code": "25rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BNE r",            "code": "26rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BEQ r",            "code": "27rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BVC r",            "code": "28rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BVS r",            "code": "29rr",             "use": "r=code_pcr"   },
    {"mnemonic": "BPL r",            "code": "2Arr",             "use": "r=code_pcr"   },
    {"mnemonic": "BMI r",            "code": "2Brr",             "use": "r=code_pcr"   },
    {"mnemonic": "BGE r",            "code": "2Crr",             "use": "r=code_pcr"   },
    {"mnemonic": "BLT r",            "code": "2Drr",             "use": "r=code_pcr"   },
    {"mnemonic": "BGT r",            "code": "2Err",             "use": "r=code_pcr"   },
    {"mnemonic": "BLE r",            "code": "2Frr",             "use": "r=code_pcr"   },
    {"mnemonic": "LEAX y",           "code": "30yy",             "use": "y_r"          },
    {"mnemonic": "LEAY y",           "code": "31yy",             "use": "y_r"          },
    {"mnemonic": "LEAS y",           "code": "32yy",             "use": "y_r"          },
    {"mnemonic": "LEAU y",           "code": "33yy",             "use": "y_r"          },
    {"mnemonic": "PSHS x",           "code": "34xx",             "use": "x=const_pshs" },
    {"mnemonic": "PULS q",           "code": "35qq",             "use": "q=const_puls" },
    {"mnemonic": "PSHU u",           "code": "36uu",             "use": "u=const_pshu" },
    {"mnemonic": "PULU v",           "code": "37vv",             "use": "v=const_pulu" },
    {"mnemonic": "RTS",              "code": "39",               "use": ""             },
    {"mnemonic": "ABX",              "code": "3A",               "use": ""             },
    {"mnemonic": "RTI",              "code": "3B",               "use": ""             },
    {"mnemonic": "CWAI b",           "code": "3Cbb",             "use": "b=const"      },
    {"mnemonic": "MUL",              "code": "3D",               "use": ""             },
    {"mnemonic": "RESET",            "code": "3E",               "use": ""             },
    {"mnemonic": "SWI",              "code": "3F",               "use": ""             },
    {"mnemonic": "NEGA",             "code": "40",               "use": ""             },
    {"mnemonic": "COMA",             "code": "43",               "use": ""             },
    {"mnemonic": "LSRA",             "code": "44",               "use": ""             },
    {"mnemonic": "RORA",             "code": "46",               "use": ""             },
    {"mnemonic": "ASRA",             "code": "47",               "use": ""             },
    {"mnemonic": "ASLA",             "code": "48",               "use": ""             },
    {"mnemonic": "LSLA",             "code": "48",               "use": ""             },
    {"mnemonic": "ROLA",             "code": "49",               "use": ""             },
    {"mnemonic": "DECA",             "code": "4A",               "use": ""             },
    {"mnemonic": "INCA",             "code": "4C",               "use": ""             },
    {"mnemonic": "TSTA",             "code": "4D",               "use": ""             },
    {"mnemonic": "CLRA",             "code": "4F",               "use": ""             },
    {"mnemonic": "NEGB",             "code": "50",               "use": ""             },
    {"mnemonic": "COMB",             "code": "53",               "use": ""             },
    {"mnemonic": "LSRB",             "code": "54",               "use": ""             },
    {"mnemonic": "RORB",             "code": "56",               "use": ""             },
    {"mnemonic": "ASRB",             "code": "57",               "use": ""             },
    {"mnemonic": "LSLB",             "code": "58",               "use": ""             },
    {"mnemonic": "ASLB",             "code": "58",               "use": ""             },
    {"mnemonic": "ROLB",             "code": "59",               "use": ""             },
    {"mnemonic": "DECB",             "code": "5A",               "use": ""             },
    {"mnemonic": "INCB",             "code": "5C",               "use": ""             },
    {"mnemonic": "TSTB",             "code": "5D",               "use": ""             },
    {"mnemonic": "CLRB",             "code": "5F",               "use": ""             },
    {"mnemonic": "NEG y",            "code": "60yy",             "use": "y_rw"         },
    {"mnemonic": "COM y",            "code": "63yy",             "use": "y_rw"         },
    {"mnemonic": "LSR y",            "code": "64yy",             "use": "y_rw"         },
    {"mnemonic": "ROR y",            "code": "66yy",             "use": "y_rw"         },
    {"mnemonic": "ASR y",            "code": "67yy",             "use": "y_rw"         },
    {"mnemonic": "ASL y",            "code": "68yy",             "use": "y_rw"         },
    {"mnemonic": "LSL y",            "code": "68yy",             "use": "y_rw"         },
    {"mnemonic": "ROL y",            "code": "69yy",             "use": "y_rw"         },
    {"mnemonic": "DEC y",            "code": "6Ayy",             "use": "y_rw"         },
    {"mnemonic": "INC y",            "code": "6Cyy",             "use": "y_rw"         },
    {"mnemonic": "TST y",            "code": "6Dyy",             "use": "y_r"          },
    {"mnemonic": "JMP y",            "code": "6Eyy",             "use": "y_r"          },
    {"mnemonic": "CLR y",            "code": "6Fyy",             "use": "y_rw"         },
    {"mnemonic": "NEG t",            "code": "70t1t0",           "use": "t=data_rw"    },
    {"mnemonic": "COM t",            "code": "73t1t0",           "use": "t=data_rw"    },
    {"mnemonic": "LSR t",            "code": "74t1t0",           "use": "t=data_rw"    },
    {"mnemonic": "ROR t",            "code": "76t1t0",           "use": "t=data_rw"    },
    {"mnemonic": "ASR t",            "code": "77t1t0",           "use": "t=data_rw"    },
    {"mnemonic": "ASL t",            "code": "78t1t0",           "use": "t=data_rw"    },
    {"mnemonic": "LSL t",            "code": "78t1t0",           "use": "t=data_rw"    },
    {"mnemonic": "ROL t",            "code": "79t1t0",           "use": "t=data_rw"    },
    {"mnemonic": "DEC t",            "code": "7At1t0",           "use": "t=data_rw"    },
    {"mnemonic": "INC t",            "code": "7Ct1t0",           "use": "t=data_rw"    },
    {"mnemonic": "TST t",            "code": "7Dt1t0",           "use": "t=data_r"     },
    {"mnemonic": "JMP t",            "code": "7Et1t0",           "use": "t=code"       },
    {"mnemonic": "CLR t",            "code": "7Ft1t0",           "use": "t=data_w"     },
    {"mnemonic": "SUBA #b",          "code": "80bb",             "use": "b=const"      },
    {"mnemonic": "CMPA #b",          "code": "81bb",             "use": "b=const"      },
    {"mnemonic": "SBCA #b",          "code": "82bb",             "use": "b=const"      },
    {"mnemonic": "SUBD #w",          "code": "83w1w0",           "use": "w=const"      },
    {"mnemonic": "ANDA #b",          "code": "84bb",             "use": "b=const"      },
    {"mnemonic": "BITA #b",          "code": "85bb",             "use": "b=const"      },
    {"mnemonic": "LDA #b",           "code": "86bb",             "use": "b=const"      },
    {"mnemonic": "EORA #b",          "code": "88bb",             "use": "b=const"      },
    {"mnemonic": "ADCA #b",          "code": "89bb",             "use": "b=const"      },
    {"mnemonic": "ORA #b",           "code": "8Abb",             "use": "b=const"      },
    {"mnemonic": "ADDA #b",          "code": "8Bbb",             "use": "b=const"      },
    {"mnemonic": "CMPX #w",          "code": "8Cw1w0",           "use": "w=const"      },
    {"mnemonic": "BSR r",            "code": "8Drr",             "use": "r=code_pcr"   },
    {"mnemonic": "LDX #w",           "code": "8Ew1w0",           "use": "w=const"      },
    {"mnemonic": "SUBA p",           "code": "90pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "CMPA p",           "code": "91pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "SBCA p",           "code": "92pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "SUBD p",           "code": "93pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "ANDA p",           "code": "94pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "BITA p",           "code": "95pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "LDA p",            "code": "96pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "STA p",            "code": "97pp",             "use": "p=data_bp_w"  },
    {"mnemonic": "EORA p",           "code": "98pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "ADCA p",           "code": "99pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "ORA p",            "code": "9App",             "use": "p=data_bp_r"  },
    {"mnemonic": "ADDA p",           "code": "9Bpp",             "use": "p=data_bp_r"  },
    {"mnemonic": "CMPX p",           "code": "9Cpp",             "use": "p=data_bp_r"  },
    {"mnemonic": "JSR p",            "code": "9Dpp",             "use": "p=code_bp"    },
    {"mnemonic": "LDX p",            "code": "9Epp",             "use": "p=data_bp_r"  },
    {"mnemonic": "STX p",            "code": "9Fpp",             "use": "p=data_bp_w"  },
    {"mnemonic": "SUBA y",           "code": "A0yy",             "use": "y_r"          },
    {"mnemonic": "CMPA y",           "code": "A1yy",             "use": "y_r"          },
    {"mnemonic": "SBCA y",           "code": "A2yy",             "use": "y_r"          },
    {"mnemonic": "SUBD y",           "code": "A3yy",             "use": "y_r"          },
    {"mnemonic": "ANDA y",           "code": "A4yy",             "use": "y_r"          },
    {"mnemonic": "BITA y",           "code": "A5yy",             "use": "y_r"          },
    {"mnemonic": "LDA y",            "code": "A6yy",             "use": "y_r"          },
    {"mnemonic": "STA y",            "code": "A7yy",             "use": "y_w"          },
    {"mnemonic": "EORA y",           "code": "A8yy",             "use": "y_r"          },
    {"mnemonic": "ADCA y",           "code": "A9yy",             "use": "y_r"          },
    {"mnemonic": "ORA y",            "code": "AAyy",             "use": "y_r"          },
    {"mnemonic": "ADDA y",           "code": "AByy",             "use": "y_r"          },
    {"mnemonic": "CMPX y",           "code": "ACyy",             "use": "y_r"          },
    {"mnemonic": "JSR y",            "code": "ADyy",             "use": "y_r"          },
    {"mnemonic": "LDX y",            "code": "AEyy",             "use": "y_r"          },
    {"mnemonic": "STX y",            "code": "AFyy",             "use": "y_w"          },
    {"mnemonic": "SUBA t",           "code": "B0t1t0",           "use": "t=data_r"     },
    {"mnemonic": "CMPA t",           "code": "B1t1t0",           "use": "t=data_r"     },
    {"mnemonic": "SBCA t",           "code": "B2t1t0",           "use": "t=data_r"     },
    {"mnemonic": "SUBD t",           "code": "B3t1t0",           "use": "t=data_r"     },
    {"mnemonic": "ANDA t",           "code": "B4t1t0",           "use": "t=data_r"     },
    {"mnemonic": "BITA t",           "code": "B5t1t0",           "use": "t=data_r"     },
    {"mnemonic": "LDA t",            "code": "B6t1t0",           "use": "t=data_r"     },
    {"mnemonic": "STA t",            "code": "B7t1t0",           "use": "t=data_w"     },
    {"mnemonic": "EORA t",           "code": "B8t1t0",           "use": "t=data_r"     },
    {"mnemonic": "ADCA t",           "code": "B9t1t0",           "use": "t=data_r"     },
    {"mnemonic": "ORA t",            "code": "BAt1t0",           "use": "t=data_r"     },
    {"mnemonic": "ADDA t",           "code": "BBt1t0",           "use": "t=data_r"     },
    {"mnemonic": "CMPX t",           "code": "BCt1t0",           "use": "t=data_r"     },
    {"mnemonic": "JSR t",            "code": "BDt1t0",           "use": "t=code"       },
    {"mnemonic": "LDX t",            "code": "BEt1t0",           "use": "t=data_r"     },
    {"mnemonic": "STX t",            "code": "BFt1t0",           "use": "t=data_w"     },
    {"mnemonic": "SUBB #b",          "code": "C0bb",             "use": "b=const"      },
    {"mnemonic": "CMPB #b",          "code": "C1bb",             "use": "b=const"      },
    {"mnemonic": "SBCB #b",          "code": "C2bb",             "use": "b=const"      },
    {"mnemonic": "ADDD #w",          "code": "C3w1w0",           "use": "w=const"      },
    {"mnemonic": "ANDB #b",          "code": "C4bb",             "use": "b=const"      },
    {"mnemonic": "BITB #b",          "code": "C5bb",             "use": "b=const"      },
    {"mnemonic": "LDB #b",           "code": "C6bb",             "use": "b=const"      },
    {"mnemonic": "EORB #b",          "code": "C8bb",             "use": "b=const"      },
    {"mnemonic": "ADCB #b",          "code": "C9bb",             "use": "b=const"      },
    {"mnemonic": "ORB #b",           "code": "CAbb",             "use": "b=const"      },
    {"mnemonic": "ADDB #b",          "code": "CBbb",             "use": "b=const"      },
    {"mnemonic": "LDD #w",           "code": "CCw1w0",           "use": "w=const"      },
    {"mnemonic": "LDU #w",           "code": "CEw1w0",           "use": "w=const"      },
    {"mnemonic": "SUBB p",           "code": "D0pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "CMPB p",           "code": "D1pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "SBCB p",           "code": "D2pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "ADDD p",           "code": "D3pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "ANDB p",           "code": "D4pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "BITB p",           "code": "D5pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "LDB p",            "code": "D6pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "STB p",            "code": "D7pp",             "use": "p=data_bp_w"  },
    {"mnemonic": "EORB p",           "code": "D8pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "ADCB p",           "code": "D9pp",             "use": "p=data_bp_r"  },
    {"mnemonic": "ORB p",            "code": "DApp",             "use": "p=data_bp_r"  },
    {"mnemonic": "ADDB p",           "code": "DBpp",             "use": "p=data_bp_r"  },
    {"mnemonic": "LDD p",            "code": "DCpp",             "use": "p=data_bp_r"  },
    {"mnemonic": "STD p",            "code": "DDpp",             "use": "p=data_bp_w"  },
    {"mnemonic": "LDU p",            "code": "DEpp",             "use": "p=data_bp_r"  },
    {"mnemonic": "STU p",            "code": "DFpp",             "use": "p=data_bp_w"  },
    {"mnemonic": "SUBB y",           "code": "E0yy",             "use": "y_r"          },
    {"mnemonic": "CMPB y",           "code": "E1yy",             "use": "y_r"          },
    {"mnemonic": "SBCB y",           "code": "E2yy",             "use": "y_r"          },
    {"mnemonic": "ADDD y",           "code": "E3yy",             "use": "y_r"          },
    {"mnemonic": "ANDB y",           "code": "E4yy",             "use": "y_r"          },
    {"mnemonic": "BITB y",           "code": "E5yy",             "use": "y_r"          },
    {"mnemonic": "LDB y",            "code": "E6yy",             "use": "y_r"          },
    {"mnemonic": "STB y",            "code": "E7yy",             "use": "y_w"          },
    {"mnemonic": "EORB y",           "code": "E8yy",             "use": "y_r"          },
    {"mnemonic": "ADCB y",           "code": "E9yy",             "use": "y_r"          },
    {"mnemonic": "ORB y",            "code": "EAyy",             "use": "y_r"          },
    {"mnemonic": "ADDB y",           "code": "EByy",             "use": "y_r"          },
    {"mnemonic": "LDD y",            "code": "ECyy",             "use": "y_r"          },
    {"mnemonic": "STD y",            "code": "EDyy",             "use": "y_w"          },
    {"mnemonic": "LDU y",            "code": "EEyy",             "use": "y_r"          },
    {"mnemonic": "STU y",            "code": "EFyy",             "use": "y_w"          },
    {"mnemonic": "SUBB t",           "code": "F0t1t0",           "use": "t=data_r"     },
    {"mnemonic": "CMPB t",           "code": "F1t1t0",           "use": "t=data_r"     },
    {"mnemonic": "SBCB t",           "code": "F2t1t0",           "use": "t=data_r"     },
    {"mnemonic": "ADDD t",           "code": "F3t1t0",           "use": "t=data_r"     },
    {"mnemonic": "ANDB t",           "code": "F4t1t0",           "use": "t=data_r"     },
    {"mnemonic": "BITB t",           "code": "F5t1t0",           "use": "t=data_r"     },
    {"mnemonic": "LDB t",            "code": "F6t1t0",           "use": "t=data_r"     },
    {"mnemonic": "STB t",            "code": "F7t1t0",           "use": "t=data_w"     },
    {"mnemonic": "EORB t",           "code": "F8t1t0",           "use": "t=data_r"     },
    {"mnemonic": "ADCB t",           "code": "F9t1t0",           "use": "t=data_r"     },
    {"mnemonic": "ORB t",            "code": "FAt1t0",           "use": "t=data_r"     },
    {"mnemonic": "ADDB t",           "code": "FBt1t0",           "use": "t=data_r"     },
    {"mnemonic": "LDD t",            "code": "FCt1t0",           "use": "t=data_r"     },
    {"mnemonic": "STD t",            "code": "FDt1t0",           "use": "t=data_w"     },
    {"mnemonic": "LDU t",            "code": "FEt1t0",           "use": "t=data_r"     },
    {"mnemonic": "STU t",            "code": "FFt1t0",           "use": "t=data_w"     },
]

POSTS = [
    {"post": "0,X",              "code": "00",               "use": ""             },
    {"post": "1,X",              "code": "01",               "use": ""             },
    {"post": "2,X",              "code": "02",               "use": ""             },
    {"post": "3,X",              "code": "03",               "use": ""             },
    {"post": "4,X",              "code": "04",               "use": ""             },
    {"post": "5,X",              "code": "05",               "use": ""             },
    {"post": "6,X",              "code": "06",               "use": ""             },
    {"post": "7,X",              "code": "07",               "use": ""             },
    {"post": "8,X",              "code": "08",               "use": ""             },
    {"post": "9,X",              "code": "09",               "use": ""             },
    {"post": "10,X",             "code": "0A",               "use": ""             },
    {"post": "11,X",             "code": "0B",               "use": ""             },
    {"post": "12,X",             "code": "0C",               "use": ""             },
    {"post": "13,X",             "code": "0D",               "use": ""             },
    {"post": "14,X",             "code": "0E",               "use": ""             },
    {"post": "15,X",             "code": "0F",               "use": ""             },
    {"post": "-16,X",            "code": "10",               "use": ""             },
    {"post": "-15,X",            "code": "11",               "use": ""             },
    {"post": "-14,X",            "code": "12",               "use": ""             },
    {"post": "-13,X",            "code": "13",               "use": ""             },
    {"post": "-12,X",            "code": "14",               "use": ""             },
    {"post": "-11,X",            "code": "15",               "use": ""             },
    {"post": "-10,X",            "code": "16",               "use": ""             },
    {"post": "-9,X",             "code": "17",               "use": ""             },
    {"post": "-8,X",             "code": "18",               "use": ""             },
    {"post": "-7,X",             "code": "19",               "use": ""             },
    {"post": "-6,X",             "code": "1A",               "use": ""             },
    {"post": "-5,X",             "code": "1B",               "use": ""             },
    {"post": "-4,X",             "code": "1C",               "use": ""             },
    {"post": "-3,X",             "code": "1D",               "use": ""             },
    {"post": "-2,X",             "code": "1E",               "use": ""             },
    {"post": "-1,X",             "code": "1F",               "use": ""             },
    {"post": "0,Y",              "code": "20",               "use": ""             },
    {"post": "1,Y",              "code": "21",               "use": ""             },
    {"post": "2,Y",              "code": "22",               "use": ""             },
    {"post": "3,Y",              "code": "23",               "use": ""             },
    {"post": "4,Y",              "code": "24",               "use": ""             },
    {"post": "5,Y",              "code": "25",               "use": ""             },
    {"post": "6,Y",              "code": "26",               "use": ""             },
    {"post": "7,Y",              "code": "27",               "use": ""             },
    {"post": "8,Y",              "code": "28",               "use": ""             },
    {"post": "9,Y",              "code": "29",               "use": ""             },
    {"post": "10,Y",             "code": "2A",               "use": ""             },
    {"post": "11,Y",             "code": "2B",               "use": ""             },
    {"post": "12,Y",             "code": "2C",               "use": ""             },
    {"post": "13,Y",             "code": "2D",               "use": ""             },
    {"post": "14,Y",             "code": "2E",               "use": ""             },
    {"post": "15,Y",             "code": "2F",               "use": ""             },
    {"post": "-16,Y",            "code": "30",               "use": ""             },
    {"post": "-15,Y",            "code": "31",               "use": ""             },
    {"post": "-14,Y",            "code": "32",               "use": ""             },
    {"post": "-13,Y",            "code": "33",               "use": ""             },
    {"post": "-12,Y",            "code": "34",               "use": ""             },
    {"post": "-11,Y",            "code": "35",               "use": ""             },
    {"post": "-10,Y",            "code": "36",               "use": ""             },
    {"post": "-9,Y",             "code": "37",               "use": ""             },
    {"post": "-8,Y",             "code": "38",               "use": ""             },
    {"post": "-7,Y",             "code": "39",               "use": ""             },
    {"post": "-6,Y",             "code": "3A",               "use": ""             },
    {"post": "-5,Y",             "code": "3B",               "use": ""             },
    {"post": "-4,Y",             "code": "3C",               "use": ""             },
    {"post": "-3,Y",             "code": "3D",               "use": ""             },
    {"post": "-2,Y",             "code": "3E",               "use": ""             },
    {"post": "-1,Y",             "code": "3F",               "use": ""             },
    {"post": "0,U",              "code": "40",               "use": ""             },
    {"post": "1,U",              "code": "41",               "use": ""             },
    {"post": "2,U",              "code": "42",               "use": ""             },
    {"post": "3,U",              "code": "43",               "use": ""             },
    {"post": "4,U",              "code": "44",               "use": ""             },
    {"post": "5,U",              "code": "45",               "use": ""             },
    {"post": "6,U",              "code": "46",               "use": ""             },
    {"post": "7,U",              "code": "47",               "use": ""             },
    {"post": "8,U",              "code": "48",               "use": ""             },
    {"post": "9,U",              "code": "49",               "use": ""             },
    {"post": "10,U",             "code": "4A",               "use": ""             },
    {"post": "11,U",             "code": "4B",               "use": ""             },
    {"post": "12,U",             "code": "4C",               "use": ""             },
    {"post": "13,U",             "code": "4D",               "use": ""             },
    {"post": "14,U",             "code": "4E",               "use": ""             },
    {"post": "15,U",             "code": "4F",               "use": ""             },
    {"post": "-16,U",            "code": "50",               "use": ""             },
    {"post": "-15,U",            "code": "51",               "use": ""             },
    {"post": "-14,U",            "code": "52",               "use": ""             },
    {"post": "-13,U",            "code": "53",               "use": ""             },
    {"post": "-12,U",            "code": "54",               "use": ""             },
    {"post": "-11,U",            "code": "55",               "use": ""             },
    {"post": "-10,U",            "code": "56",               "use": ""             },
    {"post": "-9,U",             "code": "57",               "use": ""             },
    {"post": "-8,U",             "code": "58",               "use": ""             },
    {"post": "-7,U",             "code": "59",               "use": ""             },
    {"post": "-6,U",             "code": "5A",               "use": ""             },
    {"post": "-5,U",             "code": "5B",               "use": ""             },
    {"post": "-4,U",             "code": "5C",               "use": ""             },
    {"post": "-3,U",             "code": "5D",               "use": ""             },
    {"post": "-2,U",             "code": "5E",               "use": ""             },
    {"post": "-1,U",             "code": "5F",               "use": ""             },
    {"post": "0,S",              "code": "60",               "use": ""             },
    {"post": "1,S",              "code": "61",               "use": ""             },
    {"post": "2,S",              "code": "62",               "use": ""             },
    {"post": "3,S",              "code": "63",               "use": ""             },
    {"post": "4,S",              "code": "64",               "use": ""             },
    {"post": "5,S",              "code": "65",               "use": ""             },
    {"post": "6,S",              "code": "66",               "use": ""             },
    {"post": "7,S",              "code": "67",               "use": ""             },
    {"post": "8,S",              "code": "68",               "use": ""             },
    {"post": "9,S",              "code": "69",               "use": ""             },
    {"post": "10,S",             "code": "6A",               "use": ""             },
    {"post": "11,S",             "code": "6B",               "use": ""             },
    {"post": "12,S",             "code": "6C",               "use": ""             },
    {"post": "13,S",             "code": "6D",               "use": ""             },
    {"post": "14,S",             "code": "6E",               "use": ""             },
    {"post": "15,S",             "code": "6F",               "use": ""             },
    {"post": "-16,S",            "code": "70",               "use": ""             },
    {"post": "-15,S",            "code": "71",               "use": ""             },
    {"post": "-14,S",            "code": "72",               "use": ""             },
    {"post": "-13,S",            "code": "73",               "use": ""             },
    {"post": "-12,S",            "code": "74",               "use": ""             },
    {"post": "-11,S",            "code": "75",               "use": ""             },
    {"post": "-10,S",            "code": "76",               "use": ""             },
    {"post": "-9,S",             "code": "77",               "use": ""             },
    {"post": "-8,S",             "code": "78",               "use": ""             },
    {"post": "-7,S",             "code": "79",               "use": ""             },
    {"post": "-6,S",             "code": "7A",               "use": ""             },
    {"post": "-5,S",             "code": "7B",               "use": ""             },
    {"post": "-4,S",             "code": "7C",               "use": ""             },
    {"post": "-3,S",             "code": "7D",               "use": ""             },
    {"post": "-2,S",             "code": "7E",               "use": ""             },
    {"post": "-1,S",             "code": "7F",               "use": ""             },
    {"post": ",X+",              "code": "80",               "use": ""             },
    {"post": ",X++",             "code": "81",               "use": ""             },
    {"post": ",-X",              "code": "82",               "use": ""             },
    {"post": ",--X",             "code": "83",               "use": ""             },
    {"post": ",X",               "code": "84",               "use": ""             },
    {"post": "B,X",              "code": "85",               "use": ""             },
    {"post": "A,X",              "code": "86",               "use": ""             },
    {"post": "i,X",              "code": "88ii",             "use": "i=const"      },
    {"post": "k,X",              "code": "89k1k0",           "use": "k=const"      },
    {"post": "D,X",              "code": "8B",               "use": ""             },
    {"post": "i,PC",             "code": "8Cii",             "use": "i=code_pcr"   },
    {"post": "k,PC",             "code": "8Dk1k0",           "use": "k=code_pcr"   },
    {"post": "[,X++]",           "code": "91",               "use": ""             },
    {"post": "[,--X]",           "code": "93",               "use": ""             },
    {"post": "[,X]",             "code": "94",               "use": ""             },
    {"post": "[B,X]",            "code": "95",               "use": ""             },
    {"post": "[A,X]",            "code": "96",               "use": ""             },
    {"post": "[i,X]",            "code": "98ii",             "use": "i=const"      },
    {"post": "[k,X]",            "code": "99k1k0",           "use": "k=const"      },
    {"post": "[D,X]",            "code": "9B",               "use": ""             },
    {"post": "[i,PC]",           "code": "9Cii",             "use": "i=code_pcr"   },
    {"post": "[k,PC]",           "code": "9Dk1k0",           "use": "k=code_pcr"   },
    {"post": "[t]",              "code": "9Ft1t0",           "use": "t=data"       },
    {"post": ",Y+",              "code": "A0",               "use": ""             },
    {"post": ",Y++",             "code": "A1",               "use": ""             },
    {"post": ",-Y",              "code": "A2",               "use": ""             },
    {"post": ",--Y",             "code": "A3",               "use": ""             },
    {"post": ",Y",               "code": "A4",               "use": ""             },
    {"post": "B,Y",              "code": "A5",               "use": ""             },
    {"post": "A,Y",              "code": "A6",               "use": ""             },
    {"post": "i,Y",              "code": "A8ii",             "use": "i=const"      },
    {"post": "k,Y",              "code": "A9k1k0",           "use": "k=const"      },
    {"post": "D,Y",              "code": "AB",               "use": ""             },
    {"post": "i,PC",             "code": "ACii",             "use": "i=code_pcr"   },
    {"post": "k,PC",             "code": "ADk1k0",           "use": "k=code_pcr"   },
    {"post": "[,Y++]",           "code": "B1",               "use": ""             },
    {"post": "[,--Y]",           "code": "B3",               "use": ""             },
    {"post": "[,Y]",             "code": "B4",               "use": ""             },
    {"post": "[B,Y]",            "code": "B5",               "use": ""             },
    {"post": "[A,Y]",            "code": "B6",               "use": ""             },
    {"post": "[i,Y]",            "code": "B8ii",             "use": "i=const"      },
    {"post": "[k,Y]",            "code": "B9k1k0",           "use": "k=const"      },
    {"post": "[D,Y]",            "code": "BB",               "use": ""             },
    {"post": "[i,PC]",           "code": "BCii",             "use": "i=code_pcr"   },
    {"post": "[k,PC]",           "code": "BDk1k0",           "use": "k=code_pcr"   },
    {"post": "[t]",              "code": "BFt1t0",           "use": "t=data"       },
    {"post": ",U+",              "code": "C0",               "use": ""             },
    {"post": ",U++",             "code": "C1",               "use": ""             },
    {"post": ",-U",              "code": "C2",               "use": ""             },
    {"post": ",--U",             "code": "C3",               "use": ""             },
    {"post": ",U",               "code": "C4",               "use": ""             },
    {"post": "B,U",              "code": "C5",               "use": ""             },
    {"post": "A,U",              "code": "C6",               "use": ""             },
    {"post": "i,U",              "code": "C8ii",             "use": "i=const"      },
    {"post": "k,U",              "code": "C9k1k0",           "use": "k=const"      },
    {"post": "D,U",              "code": "CB",               "use": ""             },
    {"post": "i,PC",             "code": "CCii",             "use": "i=code_pcr"   },
    {"post": "k,PC",             "code": "CDk1k0",           "use": "k=code_pcr"   },
    {"post": "[,U++]",           "code": "D1",               "use": ""             },
    {"post": "[,--U]",           "code": "D3",               "use": ""             },
    {"post": "[,U]",             "code": "D4",               "use": ""             },
    {"post": "[B,U]",            "code": "D5",               "use": ""             },
    {"post": "[A,U]",            "code": "D6",               "use": ""             },
    {"post": "[i,U]",            "code": "D8ii",             "use": "i=const"      },
    {"post": "[k,U]",            "code": "D9k1k0",           "use": "k=const"      },
    {"post": "[D,U]",            "code": "DB",               "use": ""             },
    {"post": "[i,PC]",           "code": "DCii",             "use": "i=code_pcr"   },
    {"post": "[k,PC]",           "code": "DDk1k0",           "use": "k=code_pcr"   },
    {"post": "[t]",              "code": "DFt1t0",           "use": "t=data"       },
    {"post": ",S+",              "code": "E0",               "use": ""             },
    {"post": ",S++",             "code": "E1",               "use": ""             },
    {"post": ",-S",              "code": "E2",               "use": ""             },
    {"post": ",--S",             "code": "E3",               "use": ""             },
    {"post": ",S",               "code": "E4",               "use": ""             },
    {"post": "B,S",              "code": "E5",               "use": ""             },
    {"post": "A,S",              "code": "E6",               "use": ""             },
    {"post": "i,S",              "code": "E8ii",             "use": "i=const"      },
    {"post": "k,S",              "code": "E9k1k0",           "use": "k=const"      },
    {"post": "i,X",              "code": "EAii",             "use": "i=const"      },
    {"post": "D,S",              "code": "EB",               "use": ""             },
    {"post": "i,PC",             "code": "ECii",             "use": "i=code_pcr"   },
    {"post": "k,PC",             "code": "EDk1k0",           "use": "k=code_pcr"   },
    {"post": "[,S++]",           "code": "F1",               "use": ""             },
    {"post": "[,--S]",           "code": "F3",               "use": ""             },
    {"post": "[,S]",             "code": "F4",               "use": ""             },
    {"post": "[B,S]",            "code": "F5",               "use": ""             },
    {"post": "[A,S]",            "code": "F6",               "use": ""             },
    {"post": "[i,S]",            "code": "F8ii",             "use": "i=const"      },
    {"post": "[k,S]",            "code": "F9k1k0",           "use": "k=const"      },
    {"post": "[D,S]",            "code": "FB",               "use": ""             },
    {"post": "[i,PC]",           "code": "FCii",             "use": "i=code_pcr"   },
    {"post": "[k,PC]",           "code": "FDk1k0",           "use": "k=code_pcr"   },
    {"post": "[t]",              "code": "FFt1t0",           "use": "t=data"       },
]

# TODO: LDA $FF00,PC ; PC relative


class CPU_6809(opcodetools.cpu.base_cpu.CPU):

    # 1000 1001 B,A
    # 1001 1000 B,A
    PSHS_REG_ORDER = ['PC', 'U', 'Y', 'X', 'DP', 'B', 'A', 'CC']
    REG_PAIR_WORD = ['D', 'X', 'Y', 'U', 'X', 'PC','?','?']
    REG_PAIR_BYTE = ['A', 'B', 'CC', 'DP','?','?','?','?']

    @staticmethod
    def _register_pair(value):
        a = (value>>4)&0x0F
        b = value&0x0F

        if a>7:
            a = CPU_6809.REG_PAIR_BYTE[a&7]
        else:
            a = CPU_6809.REG_PAIR_WORD[a]
        if b>7:
            b = CPU_6809.REG_PAIR_BYTE[b&7]
        else:
            b = CPU_6809.REG_PAIR_WORD[b]
        return a+','+b        

    @staticmethod
    def _register_stack(value,push=True,system=True):
        v = bin(value)[2:].rjust(8,'0')
        regs = []
        for i in range(8):
            if v[i]=='1':
                regs.append(CPU_6809.PSHS_REG_ORDER[i])
        if not system:
            if 'U' in regs:
                i = regs.index('U')
                regs[i] = 'S'
        if not push:
            regs.reverse()
        return ','.join(regs)

    def __init__(self):

        expanded_opcodes = []

        # Expand the "post" mnemonics
        for entry in OPCODES:
            if 'y' in entry['mnemonic']:
                for post in POSTS:
                    new_mnem = entry['mnemonic'].replace('y', post['post'])
                    new_code = entry['code'].replace('yy', post['code'])
                    new_entry = {'mnemonic': new_mnem,
                                 # 'code': new_code, 'bus': entry['bus']}
                                 'code': new_code, 'use': post['use']}
                    if new_entry['use']:
                        new_entry['use'] = new_entry['use'] + entry['use'][1:]
                    expanded_opcodes.append(new_entry)
            else:
                expanded_opcodes.append(entry)

        super().__init__(expanded_opcodes, False)

    def binary_to_string_fill(self, address: int, binary: list, opcode: Opcode, fills: dict, ind: int):
        # Used for disassembly
        if 'x' in opcode.use:
            s = CPU_6809._register_stack(binary[1],push=True,system=True)            
            fills['x'] = {'sub_value': s, 'visual_size': 3, 'numeric_value': 0}
        elif 'q' in opcode.use:
            s = CPU_6809._register_stack(binary[1],push=False,system=True)
            fills['q'] = {'sub_value': s, 'visual_size': 3, 'numeric_value': 0}
        elif 'u' in opcode.use:
            s = CPU_6809._register_stack(binary[1],push=True,system=False) 
            fills['u'] = {'sub_value': s, 'visual_size': 3, 'numeric_value': 0}
        elif 'v' in opcode.use:
            s = CPU_6809._register_stack(binary[1],push=False,system=False) 
            fills['v'] = {'sub_value': s, 'visual_size': 3, 'numeric_value': 0}
        elif 'z' in opcode.use:
            s = CPU_6809._register_pair(binary[1])
            fills['z'] = {'sub_value': s, 'visual_size': 3, 'numeric_value': 0}  
        else:
            super().binary_to_string_fill(address,binary,opcode,fills,ind)
        
    def fix_up_special_opcodes(self, nmatch):
        # Used in the assembly process
        if nmatch.startswith('PSHS ') or nmatch.startswith('PULS ') or nmatch.startswith('PSHU ') or nmatch.startswith('PULU '):
            regs = nmatch[5:].split(',')
            order = list(CPU_6809.PSHS_REG_ORDER)
            if nmatch[3] == 'U':
                order[1] = 'S'
            if nmatch[1] == 'U':
                order.reverse()
            order_pos = 0
            order_byte = 0
            for reg in regs:
                while True:
                    if order_pos >= len(order):
                        raise AssemblyException('Invalid push/pull register list')
                    if order[order_pos] == reg:
                        if nmatch[1] == 'S':
                            order_byte = order_byte | (128 >> order_pos)
                        else:
                            order_byte = order_byte | (1 << order_pos)
                        order_pos += 1
                        break
                    order_pos += 1
            # print('Got one to fix', hex(order_byte))
            return nmatch[:5] + str(order_byte)
        elif nmatch.startswith('EXG ') or nmatch.startswith('TFR '):
            regs = nmatch[4:].split(',')
            if len(regs) != 2:
                raise AssemblyException('Expected two registers')
            if regs[0] in CPU_6809.REG_PAIR_WORD:
                reg_set = CPU_6809.REG_PAIR_WORD
                reg_ofs = 0
            else:
                reg_set = CPU_6809.REG_PAIR_BYTE
                reg_ofs = 8
            if not regs[0] in reg_set:
                raise AssemblyException('Invalid register pair')
            i = reg_set.index(regs[0])
            reg_byte = (i | reg_ofs) << 4
            if not regs[1] in reg_set:
                raise AssemblyException('Invalid register pair')
            i = reg_set.index(regs[1])
            reg_byte = reg_byte | (i | reg_ofs)
            # print('Got one to fix', hex(reg_byte))
            return nmatch[:4] + str(reg_byte)
        return nmatch

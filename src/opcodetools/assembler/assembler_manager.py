import opcodetools.assembler.base_assembler
import opcodetools.cpu.cpu_manager

def get_assembler_by_name(name:str) -> opcodetools.assembler.base_assembler.Assembler:
    
    cp = opcodetools.cpu.cpu_manager.get_cpu_by_name(name)
    
    if name == '6502':
        return opcodetools.assembler.base_assembler.Assembler(cp)
    
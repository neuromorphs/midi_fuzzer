
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class static_multi_remap:
    kmap: Dict[str,str]= field(default_factory=lambda:({'A4':'B4', 'G4':'A5', 'C4':'D5'}))
    periodicity: int = 30
    random_length: int = 2

# @dataclass
# class schedule:
#     kmap: Dict[str,str]= field(default_factory=lambda:({'A4':'B4', 'G4':'A5', 'C4':'D5'}))
#     change_timing: List[int] = field(default_factory=lambda:([10,15,25,50]))
#     change_keys: List[List[str,str]] = field(default_factory=lambda:([['A4','B4'],['A4','C4'],['A4','D4'],['A4','E4']]))
#     random_length: int = 1

@dataclass
class random_zone_remap:
    kmap: Dict[str,str] = field(default_factory=lambda:({'C4':'C7'}))
    periodicity: int = 30
    random_length: int = 2

@dataclass
class random_zone_shift:
    kmap: Dict[str,str] = field(default_factory=lambda: {'C4':'C6'})
    periodicity: int = 30
    shift_max : int = 3
    random_length: int = 2

@dataclass
class delay_ramp:
    start_delay: int = 20 
    rate: float = .005
    shift_max : int = .2
    random_length = 2
    periodicity = 10

@dataclass
class velocity_ramp:
    start_vel: int = 1 
    start_attn: int = 3
    rate: float = .05
    shift_max : int = 6
    random_length = 2
    periodicity = 10

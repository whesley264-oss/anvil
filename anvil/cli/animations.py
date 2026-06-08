#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANVIL Loading Animations - Professional ASCII Art Loaders
These are integrated into the CLI for visual polish
"""

from __future__ import annotations

import os
import time


# ============================================
# COMPUTER SERVICES BUILDING - Setup/Deploy
# ============================================
class ComputerBuildingAnimation:
    """Computer Services Company Building"""
    
    BUILDING = """
              ,---------------------------,
              |  /---------------------\  |
              | |                       | |
              | |     Computer          | |
              | |      Services         | |
              | |       Company         | |
              | |                       | |
              |  \_____________________/  |
              |___________________________|
            ,---\_____     []     _______/------,
          /         /______________\           /|
        /___________________________________ /  | ___
        |                                   |   |    )
        |  _ _ _                 [-------]  |   |   (
        |  o o o                 [-------]  |  /    _)_
        |__________________________________ |/     /  /
    /-------------------------------------/|      ( )/
  /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    
    def __init__(self, message="Building infrastructure..."):
        self.message = message
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show(self):
        self.clear()
        print("\033[1m" + "="*52 + "\033[0m")
        print("\033[1m\033[96m Computer Services Company\033[0m\033[1m")
        print("\033[1m" + "="*52 + "\033[0m")
        print()
        print("\033[94m" + self.BUILDING + "\033[0m")
        print()
        print("\033[92m[SUCCESS] BUILDING COMPLETE!\033[0m")
        print()


# ============================================
# DOS TERMINAL - System/Doctor commands
# ============================================
class DOSTerminalAnimation:
    """Retro DOS terminal loading"""
    
    DOS = """
   ,----------------,              ,---------,           
  ,-----------------------,          ,"        ,"|           
,"                      ,"|        ,"        ,"  |           
+-----------------------+  |      ,"        ,"    |           
|  .-----------------.  |  |     +---------+      |           
|  |                 |  |  |     | -==----'|      |           
|  |  I LOVE DOS!    |  |  |     |         |      |           
|  |  Bad command or |  |  |/----|`---=    |      |           
|  |  C:>_          |  |  |   ,/|==== ooo |      ;           
|  |                 |  |  |  // |(((( [33]|    ,"            
|  |                 |," .;'| |((((     |  ,"              
|  +-----------------------+  ;;  |         |,"     -Kevin Lam-
   /_)______________(_/  //'   | +---------+                  
___________________________/___  `,                             
/  oooooooooooooooo  .o.  oooo /,   \\,"-----------               
/ ==ooooooooooooooo==.o.  ooo= //   ,`\\--{)B     ,"               
/_==__==========__==_ooo__ooo=_/'   /___________,"                 
`-----------------------------'
                              -Roland Hangg-
    """
    
    def __init__(self, message="Initializing..."):
        self.message = message
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show(self, frame=0):
        self.clear()
        print("\033[94m" + self.DOS + "\033[0m")
        
        if frame == 0:
            print("  Checking system...                     [..........] 0%")
        elif frame == 1:
            print("  Loading modules...                     [##########] 50%")
        else:
            print("\033[92m  Ready!                                [██████████] 100%\033[0m")


# ============================================
# TERMINAL WINDOW - Generic loading
# ============================================
class TerminalAnimation:
    """Modern terminal window loading"""
    
    TERMINAL = """
             ________________________________________________              
            /                                                \\             
           |    _________________________________________     |            
           |   |                                         |    |            
           |   |  C:> _                                 |    |            
           |   |                                         |    |            
           |   |                                         |    |            
           |   |                                         |    |            
           |   |                                         |    |            
           |   |                                         |    |            
           |   |_________________________________________|    |            
           |                                                  |            
            \\_________________________________________________/            
                   \\___________________________________/                   
                ___________________________________________                
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_             
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.`-_          
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_       
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_    
 _-'.-.-.-.-.-. .---.-. .-------------------------. .-.---. .---.-.-.-.`-_ 
:-------------------------------------------------------------------------:
`---._.-------------------------------------------------------------._.---'
                              -Roland Hangg-                               
    """
    
    def __init__(self, message="Processing..."):
        self.message = message
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show(self, progress=1.0):
        self.clear()
        
        filled = int(progress * 20)
        bar = "\033[92m" + "█" * filled + "\033[0m" + "░" * (20 - filled)
        
        print("\033[1m" + "="*52 + "\033[0m")
        print("\033[1m\033[96m ANVIL Terminal\033[0m\033[1m")
        print("\033[1m" + "="*52 + "\033[0m")
        print()
        print("\033[92m" + self.TERMINAL + "\033[0m")
        print()
        print("  " + self.message)
        print("  [" + bar + "] " + str(int(progress*100)) + "%")
        print()


# ============================================
# SKELETON KING - APK Build
# ============================================
class SkeletonKingAnimation:
    """Epic Skeleton King for APK builds"""
    
    SKELETON = """
                       .,,uod8B8bou,,.                             
              ..,uod8BBBBBBBBBBBBBBBBRPFT?l!i:.                    
         ,=m8BBBBBBBBBBBBBBBRPFT?!||||||||||||||                   
         !...:!TVBBBRPFT||||||||||!!^^""'   ||||                   
         !.......:!?|||||!!^^""'            ||||                   
         !.........||||  ##                 ||||                   
         !.........||||                     ||||                   
         !.........||||                     ||||                   
         !.........||||                     ||||                   
         !.........||||                     ||||                   
         `.........||||                    ,||||                   
          .;.......||||               _.-!!|||||                   
   .,uodWBBBBb.....||||       _.-!!|||||||||!:'                    
!YBBBBBBBBBBBBBBb..!|||:..-!!|||||||!iof68BBBBBb....               
!..YBBBBBBBBBBBBBBb!!||||||||!iof68BBBBBBRPFT?!::   `.             
!....YBBBBBBBBBBBBBBbaaitf68BBBBBBRPFT?!:::::::::     `.           
!......YBBBBBBBBBBBBBBBBBBBRPFT?!::::::;:!^"`;:::       `.         
!........YBBBBBBBBBBRPFT?!::::::::::^''...::::::;         iBBbo.   
`..........YBRPFT?!:::::::::::::::::;iof68BBBBb.      WBBBBbo. 
  `..........:::::::::::::::::::::::;iof688888888888b.     `YBBBP^'
    `..........:;iof688888888888888888888888888888888b.     `     
      `......::;iof688888888888888888888888888888888888b.         
        `....:::;iof688888888888888888888888888888899fT!        
          `..::!8888888888888888888888888888899fT|!^"'          
            `' !!988888888888888888888888899fT|!^"'                
                `!!8888888888888888899fT|!^"'                      
                  `!988888888899fT|!^"'                            
                    `!9899fT|!^"'                                  
    """
    
    def __init__(self, message="Forging APK..."):
        self.message = message
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show(self, progress=1.0):
        self.clear()
        
        filled = int(progress * 25)
        bar = "\033[92m" + "█" * filled + "\033[0m" + "░" * (25 - filled)
        
        print("\033[1m" + "="*52 + "\033[0m")
        print("\033[1m\033[96m ANVIL Forge\033[0m\033[1m")
        print("\033[1m" + "="*52 + "\033[0m")
        print()
        print("\033[92m" + self.SKELETON + "\033[0m")
        print()
        print("\033[93m" + self.message + "\033[0m")
        print("  [" + bar + "] " + str(int(progress*100)) + "%")
        print()
        
        if progress >= 1:
            print("\033[92m[SUCCESS] APK Forged!\033[0m")
            print()


# ============================================
# HELPERS - Quick access functions
# ============================================
def show_building():
    """Show Computer Services Building"""
    ComputerBuildingAnimation().show()

def show_terminal(progress=1.0):
    """Show Terminal Window"""
    TerminalAnimation().show(progress)

def show_skeleton(progress=1.0):
    """Show Skeleton King"""
    SkeletonKingAnimation().show(progress)

def show_dos(frame=2):
    """Show DOS Terminal"""
    DOSTerminalAnimation().show(frame)


if __name__ == "__main__":
    print("ANVIL Animation System")
    print("Commands: show_building(), show_terminal(), show_skeleton(), show_dos()")
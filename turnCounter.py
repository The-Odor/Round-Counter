from sys import argv
import sys
import tkinter as tk
import threading
import time

class TurnCounter():
    currentEffects = {}
    effectCounts = {}
    roundCounter = 1
    killList = []
    run = True

    def pprint(self):
        if len(self.currentEffects) == 0:
            return "No effect to count"
         # Counts the turns left and prints information to user
        pretty_text = ''
        for effectName in self.currentEffects:
            if self.currentEffects[effectName] == 1:
                pretty_text += "Last round of {}".format(effectName) + "\n"
            else:
                pretty_text += "{} has {} rounds left".format(effectName, self.currentEffects[effectName]) + "\n"
        return pretty_text[:pretty_text.rfind("\n")]

    def next_turn(self):
        self.roundCounter += 1
        for effectName in self.currentEffects:
            self.currentEffects[effectName] -= 1
            if(self.currentEffects[effectName] == 0):
                self.killList.append(effectName)

    def do_input(self, cmd):
            inName, inRounds = cmd[0], cmd[-1]
            if inName in self.effectCounts:
                self.currentEffects[inName + "1"] = self.currentEffects[inName]
                del self.currentEffects[inName]
                self.effectCounts[inName] += 1
                self.currentEffects[inName + str(self.effectCounts[inName])] = int(inRounds)
            else:
                self.currentEffects[inName] = int(inRounds)
                self.effectCounts[inName] = 1

    def kill_old(self):
        # KILLS THE UNWANTED. fr tho removes finished sequences from dictionaries
        for effectName in self.killList:
            del self.currentEffects[effectName]
            trueEffect = "".join(i for i in effectName if not i.isdigit())
            self.effectCounts[trueEffect] -= 1
            if self.effectCounts[trueEffect] == 0:
                del self.effectCounts[trueEffect]
        self.killList.clear()             


    def run(self):
        while self.run:
            # Interprets input and puts info into both dictionaries
            cmd = input("\n\n\nTurn {}; What happens? ".format(self.roundCounter)).split(":")

            while len(cmd) > 1:
                self.do_input(cmd)
                cmd = input("Anything else? ").split(":")
            if(cmd[0].lower() == 'q'):
                self.run = False
            
            print(self.pprint())
            self.next_turn()
            self.kill_old()



class GUIInterface(TurnCounter):

    def add_effect(self, event):
        cmd = self.entry.get().split(":")
        self.do_input(cmd)
        self.update_gui()

    def next_turn_gui(self, event):
        self.next_turn()
        self.kill_old()
        self.update_gui()
    
    def run(self):
        self.window = tk.Tk()
        self.window.title("Tabletop Turn Counter")
        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)
        self.entry = tk.Entry(self.window)
        self.add_effect_btn = tk.Button(self.window, text="Add new effect!")
        self.add_effect_btn.bind("<Button-1>", self.add_effect)

        self.next_turn_btn = tk.Button(self.window, text="Next Turn!")
        self.next_turn_btn.bind("<Button-1>", self.next_turn_gui)

        self.display_text = tk.StringVar()
        self.info_text = tk.Label(self.window, textvariable=self.display_text)

        self.entry.pack()
        self.add_effect_btn.pack()
        self.next_turn_btn.pack()
        self.info_text.pack()

        self.window.mainloop()
    
    def update_gui(self):
        current = "It is turn {}\n".format(self.roundCounter)
        self.display_text.set(current + self.pprint())


if __name__ == "__main__":
    if "--nogui" in argv:
        print("""Turn counter for spells and effects!
            Usage: Input two arguments; name of effects and turns to last.
            If you put in nothing, a turn advances and counters count
            Example: Greater Flaming Sphere: 7
            (input argument is split at ':' )""")
        tc = TurnCounter()
        tc.run()
        sys.exit(0)

    tc = GUIInterface()
    tc.run()


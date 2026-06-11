from collections import defaultdict

class WordCount:
    def __init__(self):
        self.total_count = defaultdict(int)
        
    def analyze(self):
        sentence = input("type a sentence: ")
        words = sentence.split()
        try:
            for word in words:
                self.total_count[word.strip(" ,.-:;\'\"\n").lower()] += 1
        except:
            raise
        finally:
            print(f"{len(words): >3} words processed")

    def view_count(self):

        if not len(self.total_count):
            print("nothing to show")
            return None

        print("word" + " " * 8 + " val\n" + "="*16)
        for k, v in self.total_count.items():
            print(f"{k: <12} {v: >3d}")


    def view_frequency(self, n=0):

        if not len(self.total_count):
            print("nothing to show")
            return None
        if not n:
            n = len(self.total_count)

        s = sorted(self.total_count.items(), key=lambda item: item[1], reverse=True)
        print(f"top {n} frequency words")
        print("word" + " " * 8 + " val\n" + "="*16)
        for i in range(0,n):
            print(f"{s[i][0]: <12} {s[i][1]: >3d}")

    def lookup(self):
        word = input("search for word: ")
        print()

        if word in self.total_count:
            print(f"{word: <12} {self.total_count[word]: >3d}")
        else:
            print("not found")
        
    def clear_all(self):
        print(f"clearing {len(self.total_count)} words")
        self.total_count.clear()

def print_menu(*args:str) -> None:
    """
    print main menu from list
    """
    print()
    for idx, item in enumerate(args, 1):
        print(f"{idx}. {item}")
    print(f"0. exit")

def get_selection(lim:int = 0) -> int:
    """
    get selection from user, return int within limit
    - repeat on ValueError
    """
    valid = False
    while not valid:
        try:
            sel = int(input(f"select a number between 1-{lim}: "))
        except ValueError:
            print("bad value")
            continue
        except Exception as e:
            raise e
        print()
        match sel:
            case sel if sel < 0 :
                print("value too low")
                valid = False
            case sel if sel > lim:
                print("value too hight")
                valid = False
            case _:
                valid = True
    return sel

if __name__ == "__main__":
    TOP_N_FREQ = 3
    menu_options = {1: "Analyse a sentence", 
                    2: "View word counts", 
                    3: "View most frequent word", 
                    4: "View all by Frequency",
                    5: "Search for a Word",
                    6: "Clear results"}
    wc = WordCount()

    print_menu(*menu_options.values())
    while user_selection := get_selection(len(menu_options)):
        match user_selection:
            case 1: # analyze
                wc.analyze()
            case 2: # view counts
                wc.view_count()
            case 3: # most frequent
                wc.view_frequency(TOP_N_FREQ)
            case 4: # clear
                wc.view_frequency()
            case 5:
                wc.lookup()
            case 6:
                wc.clear_all()
            case 0: # exit
                pass
        print_menu(*menu_options.values())
    print("exiting...")
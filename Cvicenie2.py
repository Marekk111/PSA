#!/usr/bin/env python111
APP_VERSION = "1.0"

class Movie:
    def __init__(self, paTitle, paYear, paGenre, paEarnings, paRating, paDuration):
        self.aTitle = paTitle
        self.aYear = paYear
        self.aGenre = paGenre
        self.aEarnings = paEarnings
        self.aRating = paRating
        self.aDuration = paDuration
    
    def toString(self):
        return "{:20} {:4} {:10} $M{:3} {:3}% {:3}m".format(self.aTitle, 
                                                        self.aYear, 
                                                        self.aGenre, 
                                                        self.aRating, 
                                                        self.aDuration)

class MovieLibrary:
    def __init__(self):
        self.aLibrary = list()

    def addMovie(self, paMovie):
        self.aLibrary.append(paMovie)
    def removeMovie(self, paMovieIndex):
        self.aLibrary.pop(paMovieIndex)
    def printLibrary(self, paPrintIndex):
        if paPrintIndex:
            indexString = " ID "
        else:
            indexString = ""

        header = "{}{:20} {:4} {:10} {:5} {:4} {:4}".format(indexString,
                                                        "Title",
                                                        "Year",
                                                        "Genre",
                                                        "Earn"
                                                        "RATE",
                                                        "Time")
        print(header)
        print("-"*len(header))
        
        index = 0
        for movie in self.aLibrary:
            if paPrintIndex:
                print("{}. {}".format(index, movie.toString()))
            else:
                print(movie.toString())

            index += 1        

                

def menu(paMovieLibrary):
    while True:

        print ("Welcome to Movie Library v{}".format(APP_VERSION))
        print(" Add Movie (1)")
        print(" Remove Movie (2)")
        print(" Show library content (3)")
        print(" End program (q)")
        opt = input(" Select an option from the menu: ")

        if opt == "1":
            addMovie(paMovieLibrary)
        elif opt == "2":
            removeMovie(paMovieLibrary)
        elif opt == "3":
            showContent(paMovieLibrary)
        elif opt == "q":
            print("Bye! Thank for using my program.")
            exit(0)
        else:
            print("No such option exists.")

def addMovie(paMovieLibrary):
    title = input("Enter movie title: ")
    year = input("Enter movie year: ")
    genre = input("Enter movie genre: ")
    earnings = input("Enter movie earnings in $mil : ")
    rating = input("Enter movie rating: ")
    duration = input("Enter movie duration in minutes: ")
    paMovie = Movie(title, year, genre, earnings, rating, duration)
    paMovieLibrary.addMovie(paMovie)

def removeMovie(paMovieLibrary):
    paMovieLibrary.printLibrary(True)
    index = input("Enter movie index for removal: ")
    paMovieLibrary.removeMovie(eval(index))

def showContent(paMovieLibrary):
    paMovieLibrary.printLibrary(True)

if __name__ == "__main__":
    library = MovieLibrary()
    menu(library)
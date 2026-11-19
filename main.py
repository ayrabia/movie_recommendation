from load_data import load_movies
from queries import find_by_title, movies_in_genre

def main():
    #load the user input
    df = load_movies()

    print("Movie Explorer")
    print("Commands: search <title>, genre <genre>, help, quit")

    while True:
        user_input = input("\nEnter a Command: ").strip()

        if not user_input:
            continue

        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()

        if command == "quit":
            print("Goodbye")
            break

        elif command == "help":
            print("search <title> - search a movie by it's title")
            print("genre <genre> - search for movies in a genre")
            print("quit - exit the program")

        elif command in ["search", "genre"]:
            #if no title or genre is included
            if len(parts) < 2:
                print("Please include a movie title or genre")
                continue

            query = parts[1]
            if command == "search":
                result = find_by_title(df, query)
            else:
                result = movies_in_genre(df, query)

            if result.empty:
                print("No results found.")
            else:
                #.to_string(index=False) turns the DataFrame into readable text and hides the row index
                print(result.head(20).to_string(index = False))

        else:
            print("Unknown Command.")

if __name__ == "__main__":
    main()
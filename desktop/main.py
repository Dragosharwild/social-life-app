from tkinter import Tk, Label

def main():
    root = Tk()
    root.title("Social Life App - Desktop")
    root.geometry("400x300")
    
    label = Label(root, text="Welcome to the App")
    label.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
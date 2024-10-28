import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests

class WebScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrapeur Web")

        # Variables for URL, Tag, Class, and ID
        self.url_var = tk.StringVar()
        self.tag_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.id_var = tk.StringVar()

        # Create and place labels and entry widgets
        tk.Label(root, text="URL:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.url_var, width=40).grid(row=0, column=1, padx=5, pady=5, columnspan=3)

        tk.Label(root, text="Balise:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.tag_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Class:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.class_var).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(root, text="ID:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.id_var).grid(row=2, column=1, padx=5, pady=5)

        # Create and place buttons
        tk.Button(root, text="Scrape et Enregistre ", command=self.scrape_and_save).grid(row=3, column=1, pady=10, columnspan=3)

    def scrape_and_save(self):
        # Get values from entry widgets
        url = self.url_var.get()
        tag = self.tag_var.get()
        class_ = self.class_var.get()
        id_ = self.id_var.get()

        # Scrape website
        scraped_text = self.scrape_website(url, tag, class_, id_)

        # Save scraped text to a file
        self.save_to_file(scraped_text)

    def scrape_website(self, url, tag, class_, id_):
        try:
            # Send an HTTP request to the specified URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content of the page
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find elements based on tag, class, and/or ID
                elements = soup.find_all(tag, class_=class_, id=id_)

                # Extract and return the text from the found elements
                return '\n\n'.join([element.get_text() for element in elements])
            else:
                messagebox.showerror("Error", f"Failed to retrieve the page. Status Code: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_to_file(self, text):
        try:
            # Ask user for the file name and location
            #file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        
            default_file_name = "Scrapped.txt"

            # Get the script's directory
            script_directory = os.path.dirname(os.path.realpath(__file__))

            # Create the file path
            file_path = os.path.join(script_directory, default_file_name)

            # If the user cancels the dialog, return
            if not file_path:
                return
            

            # Write the scraped text to the file
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(text)

            messagebox.showinfo("Success", "Le texte scrappé est enregistré dans le fichier")
        except Exception as e:
            messagebox.showerror("Error", f"Erreur lors de l'enregistremement : {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperGUI(root)
    root.mainloop()

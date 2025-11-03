import os
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog , messagebox
import webbrowser

class SteganogeraphyApp:
    def __init__(self, root):
        """
        Initialize the application with the main window

        Args:
        root: The main CTk window object
        """
        self.root = root 
        self.root.title("Image Steganography")
        self.root.geometry("700x600")

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.image_path = None 
        self.output_path = None

        self.setup_ui()


    def setup_ui(self):

        title = ctk.CTkLabel(
            self.root, 
            text= "Steganography App",
            font= ctk.CTkFont(size= 24, weight= "bold")
        )
        title.pack(pady= 20)
        self.tabview = ctk.CTkTabview(
            self.root,
            width= 650,
            height= 450
        )
        self.tabview.pack(padx= 20, pady= 10)

        self.tabview.add("ENcode")
        self.tabview.add("DEcode")

        self.setup_encode_tab()
        self.setup_decode_tab()

        self.setup_footer()

    def setup_encode_tab(self):

        tab = self.tabview.tab("ENcode")

        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(padx= 20 ,pady= 10, fill="x")
        
        # === IMAGE SELECTION SECTION ===

        self.encode_btn = ctk.CTkButton(
            btn_frame,
            text = "Select Image",
            command=self.select_encode_image
        )
        self.encode_btn.pack(side= "left", padx= 5)

        self.encode_lable = ctk.CTkLabel(
            btn_frame,
            text= "No image selected!"
        )
        self.encode_lable.pack(side= "left", padx= 10)

        # === TEXT INPUT SECTION ===

        text_label = ctk.CTkLabel(
            tab,
            text= "Inter your text to hide!",
            font= ctk.CTkFont(size= 14)
        )
        text_label.pack(pady= (20 ,5))
        
        self.text_input = ctk.CTkTextbox(
            tab,
            height= 200,
            width= 600
        )
        self.text_input.pack(padx= 20, pady= 5)

        # === ENCODE ACTION SECTION ===

        self.encode_action_btn = ctk.CTkButton(
            tab,
            text= "ENcode & Save",
            command= self.encode_message,
            font= ctk.CTkFont(size= 14)
        )
        self.encode_action_btn.pack(pady= 20)

        self.encode_status = ctk.CTkLabel(
            tab,
            text="", 
            text_color="green" 
        )
        self.encode_status.pack()

    def setup_decode_tab(self):

        tab = self.tabview.tab("DEcode")

        # === IMAGE SELECTION SECTION ===
        
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(padx= 20 ,pady= 10, fill="x")

        self.decode_btn = ctk.CTkButton(
            btn_frame,
            text= "Select encoded image",
            command= self.select_decode_image
        )
        self.decode_btn.pack(side= "left", padx= 5)

        self.decode_label = ctk.CTkLabel(
            btn_frame,
            text= "No image selected!"
        )
        self.decode_label.pack(side= "left", padx= 10)

        # === DECODE ACTION SECTION ===

        self.decode_action_btn = ctk.CTkButton(
            tab,
            text = "decode message",
            command= self.decode_message,
            font= ctk.CTkFont(size= 14)
        )
        self.decode_action_btn.pack(pady= 20)

        # === OUTPUT DISPLAY SECTION ===

        output_label = ctk.CTkLabel(
            tab,
            text="Hidden Text: ", 
            font=ctk.CTkFont(size=14)
        )
        output_label.pack(pady=(10, 5))

        self.text_output = ctk.CTkTextbox(
            tab,
            width=600, 
            height=200 
        )
        self.text_output.pack(padx=20, pady=5)

    def setup_footer(self):
        """
        Create footer section with author information at the bottom
        """
        footer_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        footer_frame.pack(side="bottom", pady=10)
        
        author_label = ctk.CTkLabel(
            footer_frame,
            text="Created by Ali Morsali | © 2025",  
            font=ctk.CTkFont(size=11),
            text_color="gray",
            cursor= "hand2"  
        )
        def on_enter(e):
            author_label.configure(text_color= "#1E90FF")
        
        def on_leave(e):
            author_label.configure(text_color= "gray")
        author_label.pack()
        author_label.bind("<Enter>", on_enter)
        author_label.bind("<Leave>", on_leave)
        author_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/kindterrorist"))

    def select_encode_image(self):
        """
        Open file dialog for user to select an image to encode a message into
        """
        path = filedialog.askopenfilename(
            filetypes= [("Image files" , " *.jpg *.png *.jpeg *.bmp ")]
        )

        if path:
            self.image_path = path
            self.encode_lable.configure(text= os.path.basename(path))
            self.encode_status.configure(text="")

    def select_decode_image(self):
        """
        Open file dialog for user to select an encoded image to decode
        Note: Only PNG files work because JPEG compression destroys hidden data
        """
        path = filedialog.askopenfilename(
            filetypes= [("PNG files" , "*.png")]
        )

        if path:
            self.output_path = path
            self.decode_label.configure(text= os.path.basename(path))

    def encode_message(self):
        """
        Main function to encode a text message into an image
        Validates inputs, performs encoding, and saves the result
        """
        if not self.image_path:
            messagebox.showerror("Error", "please select a picture!")
            return
        
        # "1.0" means line 1, character 0 (start)
        # "end-1c" means end minus 1 character (excludes final newline)
        message = self.text_input.get("1.0", "end-1c")

        if not message:
            messagebox.showerror("Error", "please inter your text!")
            return
        
        try:
            img = Image.open(self.image_path)

            encoded_img = self.encode_text_in_image(img ,message)

            save_path = filedialog.asksaveasfilename(
                defaultextension= ".png",
                filetypes= [("PNG files", "*.png")] #.png is lossless
            )

            if save_path:
                encoded_img.save(save_path, "PNG")

                self.encode_status.configure(
                    text= f"✓ Message encoded successfully!"
                )

                messagebox.showinfo(
                    title= "successful!",
                    message= "Message encoded and saved successfully!"
                )

        except Exception as e:
            messagebox.showerror(f"Error", "encoding failed: {str(e)}" )

    def decode_message(self):
        """
        Main function to decode a hidden message from an encoded image
        """

        if not self.output_path:
            messagebox.showerror("Error", "please select an image!")
            return
        
        try:
            img = Image.open(self.output_path)

            decoded_text = self.decode_text_from_image(img)

            self.text_output.delete("1.0", "end")
            self.text_output.insert(1.0, decoded_text)

            if decoded_text:
                messagebox.showinfo("SUCCESS!", "message decoded successfully!")
            else:
                messagebox.showerror("Error", "no hidden message found!")
        except Exception as e:
            messagebox.showerror(f"Error", "encoding failed: {str(e)}")

    def encode_text_in_image(self, img, text):
        """
        Core encoding algorithm: hides text in image pixels using LSB steganography

        Args:
        img: PIL Image object to encode text into
        text: String message to hide

        Returns:
        Modified PIL Image with hidden text

        How it works:
        1. Converts each character to 8-bit binary using ord()
        2. Modifies the least significant bit (LSB) of RGB values
        3. Spreads the message across pixels in the image
        """

        text = text + "<<<END>>>" #mark the end of text

        if img.mode != 'RGB':
            img = img.convert('RGB')

        pixels = img.load()

        width, height = img.size

        # '08b' means: 8 digits, binary format, zero-padded
        binary_message = ''.join(format(ord(char), '08b') for char in text)

        # Each pixel has 3 channels (RGB), so 3 bits per pixel
        if len(binary_message) > width * height * 3:
            raise ValueError("Message too long for this picture!" \
            "select an Image with more pixels.")
        
        data_index = 0

        for y in range(height):
            for x in range(width):
                if data_index >= len(binary_message):
                    return img
                
                r, g, b = pixels[x, y]

                if data_index < len(binary_message):
                    # Binary AND with 0xFE (11111110) clears the last bit
                    # Then OR with our message bit to set it
                    # Example: r=10101010, bit=1 -> (10101010 & 11111110) | 1 = 10101011

                    # Encode one bit in the Red channel
                    r = (r & 0xFE) | int(binary_message[data_index])
                    data_index += 1 

                # Encode one bit in the Green channel
                if data_index < len(binary_message):
                    g = (g & 0xFE) | int(binary_message[data_index])
                    data_index += 1

                # Encode one bit in the Blue channel
                if data_index < len(binary_message):
                    b = (b & 0xFE) | int(binary_message[data_index])
                    data_index += 1

                # Write the modified RGB values back to the pixel
                pixels[x, y] = (r, g, b)

        return img
    
    def decode_text_from_image(self, img):
        """
        Core decoding algorithm: extracts hidden text from image pixels

        Args:
        img: PIL Image object containing hidden text

        Returns:
        Decoded text message as a string

        How it works:
        1. Reads the LSB from each RGB channel of every pixel
        2. Reconstructs binary string from these bits
        3. Converts binary back to characters using chr()
        4. Stops when it finds the end delimiter
        """
        if img.mode != "RGB":
            return messagebox.showerror("Error", "Image may have been converted! cannot access!")
        
        pixels = img.load()

        width, height = img.size 

        binary_message = ""

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
            
                # Binary AND with 1 gets only the last bit
                # Example: 10101011 & 00000001 = 00000001 = 1

                # Extract the least significant bit from Red channel
                binary_message += str(r & 1)

                # Extract LSB from Green channel
                binary_message += str(g & 1)

                # Extract LSB from Blue channel
                binary_message += str(b & 1)

        message = ""

        # Process binary string in chunks of 8 bits (1 byte = 1 character)
        for i in range(0, len(binary_message), 8):
            # Get 8-bit chunk (one byte)
            byte = binary_message[i:i+8]

            # Make sure we have a complete byte (8 bits)
            if len(byte) == 8:
                # Convert binary string to integer, then to character
                # Example: '01000001' -> int('01000001', 2) = 65 -> chr(65) = 'A'
                char = chr(int(byte, 2))

                message += char

                # endswith() checks the last characters of the string
                if message.endswith("<<<END>>>"):
                    return message[:-9]

        return message


        
if __name__ == "__main__":
    root = ctk.CTk()
    app = SteganogeraphyApp(root)
    root.mainloop()
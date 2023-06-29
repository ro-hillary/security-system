import customtkinter as ctk
from PIL import Image
from processor import Processor

# Configure application theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# App class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Entity identifier")
        self.geometry(f"{1024}x{640}")

        # Configure grid layout (4x4)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create topbar frame with widgets
        self.topbar_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.topbar_frame.grid(row=0, column=0, sticky="nsew")

        # Create the work area frame
        self.workarea_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='transparent')
        self.workarea_frame.grid(row=1, column=0, sticky="nsew")

        # Create footer frame
        self.footer_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.footer_frame.grid(row=2, column=0, sticky="nsew")

        # Top bar elements
        self.topbar_title_label = ctk.CTkLabel(self.topbar_frame, text='CAPTURA DE VIDEO EN TIEMPO REAL')
        self.topbar_title_label.pack(pady=5, padx=5)

        # Work area elements
        self.workarea_video_label = ctk.CTkLabel(self.workarea_frame, text='', image=None)
        self.workarea_video_label.pack(pady=10, padx=5)

        self.workarea_scan_button = ctk.CTkButton(self.workarea_frame, text='Scan', command=self.scan_frame)
        self.workarea_scan_button.pack(pady=(10, 5), padx=5)

        self.workarea_result_textbox = ctk.CTkLabel(self.workarea_frame, text='',width=192, height=28)
        self.workarea_result_textbox.pack(pady=(5, 10), padx=5)

        # Footer elements
        self.footer_info_label = ctk.CTkLabel(self.footer_frame, text='By R&R')
        self.footer_info_label.pack(pady=5, padx=5)

        # Processor
        self.processor = Processor(640, 480, 384, 48)

        # Start updating video
        self.update_video_label()

    def update_video_label(self):
        """Update image label"""
        image_array = self.processor.visualize()
        self.workarea_video_label.configure(image=ctk.CTkImage(Image.fromarray(image_array, 'RGB'), size=(640, 480)))

        # Continue updating video...
        self.after(40, self.update_video_label)

    def quit_label(self):
        """Set the label text to blank"""
        self.workarea_result_textbox.configure(text='')

    def scan_frame(self):
        """Capture the current frame and process it"""
        dni = self.processor.get_id()

        if dni == 'Not Allowed!' or dni == 'Try again':
            self.workarea_result_textbox.configure(text=dni, text_color="red")
            app.after(1500, self.quit_label)
        else:
            self.workarea_result_textbox.configure(text=dni, text_color="green")
            app.after(1500, self.quit_label)


if __name__ == "__main__":
    app = App()
    app.mainloop()

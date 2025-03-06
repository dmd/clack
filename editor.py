#!/usr/bin/env python3

import tkinter as tk
import numpy as np
import sys
from clack import blank_screen, clack_post, WIDTH, HEIGHT

class ClackTkEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Clack Display Editor")
        
        # Initialize the display grid - using transposed orientation
        # The physical display is actually WIDTH=28, HEIGHT=14
        # But our logical representation is keeping it consistent with the API
        self.screen = blank_screen(HEIGHT, WIDTH)  # Make sure orientation matches physical display
        self.cell_size = 25  # Size of each cell in pixels
        self.drawing = False
        self.current_mode = 'draw'  # 'draw' or 'erase'
        self.is_rotated = False  # Track the rotation state
        
        # Create frame for the grid
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)
        
        # Create canvas for the grid - default orientation is WIDTH=28, HEIGHT=14
        self.canvas = tk.Canvas(
            self.frame, 
            width=WIDTH*self.cell_size, 
            height=HEIGHT*self.cell_size,
            bg='black'
        )
        self.canvas.pack()
        
        # Create cells on the canvas
        self.cells = {}
        for y in range(HEIGHT):
            for x in range(WIDTH):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                cell = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill='black', outline='gray', width=1,
                    tags=f"cell_{x}_{y}"
                )
                self.cells[(x, y)] = cell
        
        # Create buttons frame
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)
        
        # Create Clear button
        self.clear_button = tk.Button(
            self.button_frame,
            text="Clear Grid",
            command=self.clear_grid
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Create Rotate button
        self.rotate_button = tk.Button(
            self.button_frame,
            text="Rotate Display",
            command=self.rotate_display
        )
        self.rotate_button.pack(side=tk.LEFT, padx=5)
        
        # Create Flip Horizontal button
        self.flip_h_button = tk.Button(
            self.button_frame,
            text="Flip Horizontal",
            command=self.flip_horizontal
        )
        self.flip_h_button.pack(side=tk.LEFT, padx=5)
        
        # Create Flip Vertical button
        self.flip_v_button = tk.Button(
            self.button_frame,
            text="Flip Vertical",
            command=self.flip_vertical
        )
        self.flip_v_button.pack(side=tk.LEFT, padx=5)
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Render the initial grid
        self.update_display()
    
    def get_cell_coords(self, event):
        """Convert canvas coordinates to grid coordinates"""
        # Get the current dimensions of the screen
        current_height, current_width = self.screen.shape
        
        # Simple conversion from screen coordinates to grid coordinates
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        
        # Make sure we don't exceed the bounds
        if x >= current_width:
            x = current_width - 1
        if y >= current_height:
            y = current_height - 1
            
        return x, y
    
    def on_mouse_down(self, event):
        self.drawing = True
        x, y = self.get_cell_coords(event)
        
        # Get the current dimensions of the screen
        current_height, current_width = self.screen.shape
        
        # Ensure coordinates are within bounds
        if not (0 <= x < current_width and 0 <= y < current_height):
            return
            
        # Set current_mode based on first clicked cell - inverse of current state
        if self.screen[y, x] == b'.':
            self.current_mode = 'draw'
        else:
            self.current_mode = 'erase'
            
        self.toggle_cell(x, y)
    
    def on_mouse_drag(self, event):
        if not self.drawing:
            return
            
        x, y = self.get_cell_coords(event)
        
        # Get the current dimensions of the screen
        current_height, current_width = self.screen.shape
        
        # Ensure coordinates are within bounds
        if not (0 <= x < current_width and 0 <= y < current_height):
            return
            
        # Get the current state of the cell
        current_state = self.screen[y, x].decode('utf-8')
        
        # If the cell state doesn't match our current mode, toggle it
        # This ensures continuous drawing/erasing behavior
        if (self.current_mode == 'draw' and current_state == '.') or \
           (self.current_mode == 'erase' and current_state == 'x'):
            self.toggle_cell(x, y)
    
    def on_mouse_up(self, event):
        self.drawing = False
    
    def toggle_cell(self, x, y):
        """Toggle a cell between on and off"""
        # Get the current dimensions of the screen
        current_height, current_width = self.screen.shape
        
        # Ensure coordinates are within bounds
        if not (0 <= x < current_width and 0 <= y < current_height):
            return
            
        if self.current_mode == 'draw':
            self.screen[y, x] = b'x'
            self.canvas.itemconfig(self.cells[(x, y)], fill='white')
        else:  # erase mode
            self.screen[y, x] = b'.'
            self.canvas.itemconfig(self.cells[(x, y)], fill='black')
        
        # Update the display immediately after each cell change
        self.post_to_display()
    
    def update_display(self):
        """Update the display grid based on the screen state"""
        current_height, current_width = self.screen.shape
        
        for y in range(current_height):
            for x in range(current_width):
                if self.screen[y, x] == b'.':
                    self.canvas.itemconfig(self.cells[(x, y)], fill='black')
                else:
                    self.canvas.itemconfig(self.cells[(x, y)], fill='white')
    
    def clear_grid(self):
        """Clear the entire grid"""
        # Get current dimensions to maintain the same orientation
        current_height, current_width = self.screen.shape
        self.screen = blank_screen(current_height, current_width)
        self.update_display()
        self.post_to_display()
    
    def rotate_display(self):
        """Rotate the display 90 degrees - swap WIDTH (28) and HEIGHT (14)"""
        # Swap WIDTH and HEIGHT for canvas dimensions
        self.is_rotated = not self.is_rotated
        
        # Rotate the matrix by using numpy's transpose
        self.screen = np.transpose(self.screen)
        
        # Create a new canvas with swapped dimensions
        self.canvas.destroy()
        
        if self.is_rotated:
            self.canvas = tk.Canvas(
                self.frame, 
                width=HEIGHT*self.cell_size, 
                height=WIDTH*self.cell_size,
                bg='black'
            )
        else:
            self.canvas = tk.Canvas(
                self.frame, 
                width=WIDTH*self.cell_size, 
                height=HEIGHT*self.cell_size,
                bg='black'
            )
            
        self.canvas.pack()
        
        # Recreate cells on the canvas
        self.cells = {}
        current_height, current_width = self.screen.shape
        
        for y in range(current_height):
            for x in range(current_width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill='black' if self.screen[y, x] == b'.' else 'white', 
                    outline='gray', 
                    width=1,
                    tags=f"cell_{x}_{y}"
                )
                self.cells[(x, y)] = cell
                
        # Rebind mouse events
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Post to display
        self.post_to_display()
    
    def flip_horizontal(self):
        """Flip the display horizontally (left/right)"""
        # Get current dimensions and flip along the width axis
        current_height, current_width = self.screen.shape
        
        # Create a new array with flipped content
        for y in range(current_height):
            self.screen[y] = self.screen[y][::-1]  # Reverse each row
            
        # Update the visual display
        self.update_display()
        
        # Update the physical display
        self.post_to_display()
        
    def flip_vertical(self):
        """Flip the display vertically (up/down)"""
        # Get current dimensions and flip along the height axis
        current_height, current_width = self.screen.shape
        
        # Create a new array with flipped content
        self.screen = self.screen[::-1]  # Reverse the rows
            
        # Update the visual display
        self.update_display()
        
        # Update the physical display
        self.post_to_display()
    
    def post_to_display(self):
        """Post the current state to the clack display"""
        # Create a rotated version of the screen for posting to match the physical display
        # This rotates the content 180 degrees to correct the orientation
        rotated_screen = np.rot90(self.screen, k=2)  # Rotate 180 degrees (k=2)
        screen_bytes = b'\n'.join([b''.join(row) for row in rotated_screen])
        clack_post(screen_bytes)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClackTkEditor(root)
    root.mainloop()
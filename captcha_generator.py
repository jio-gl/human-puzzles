import random
import math
import io
import base64
import hashlib

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow is not installed. Please install it using 'pip install pillow'")
    # Provide mock implementations or exit gracefully
    import sys
    sys.exit(1)

class GeometricCaptcha:
    def __init__(self, width=720, height=720, seed=None):
        self.width = width
        self.height = height
        self.seed = seed if seed else hashlib.md5(str(random.random()).encode()).hexdigest()
        self.rng = random.Random(self.seed)
        
        # Create a white background
        self.image = Image.new('RGB', (width, height), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        
        # Grid parameters - more organized but still with some randomness
        self.cell_size = 45  # Keep cell size the same
        self.grid_jitter = 5  # Reduced jitter for more grid-like appearance
        self.rows = 16  # Fixed to 16 rows
        self.cols = 16  # Fixed to 16 columns
        
        # Pacman parameters
        self.pacman_radius = self.cell_size * 0.33  # Smaller pacman shapes
        
        # Emergent patterns
        self.emergent_shapes = []
        self.expected_count = 0
        
        # Some "taken" positions to avoid overlap
        self.taken_positions = set()
        
        # Try to use a default font, or fallback to default
        try:
            self.font = ImageFont.truetype("Arial", 10)
        except IOError:
            self.font = ImageFont.load_default()
    
    def add_grid_coordinates(self):
        """Add grid coordinate numbers along the X and Y axes"""
        # Draw column numbers (X-axis)
        for col in range(self.cols):
            x = col * self.cell_size + self.cell_size // 2
            # At the top
            self.draw.text((x, 5), str(col), fill=(150, 150, 150), font=self.font, anchor="mt")
            # At the bottom
            self.draw.text((x, self.height - 5), str(col), fill=(150, 150, 150), font=self.font, anchor="mb")
        
        # Draw row numbers (Y-axis)
        for row in range(self.rows):
            y = row * self.cell_size + self.cell_size // 2
            # On the left
            self.draw.text((5, y), str(row), fill=(150, 150, 150), font=self.font, anchor="lm")
            # On the right
            self.draw.text((self.width - 5, y), str(row), fill=(150, 150, 150), font=self.font, anchor="rm")
    
    def create_pacman(self, x, y, angle1, angle2, radius=None):
        """
        Create a black pacman shape with an arbitrary angle cutout
        angle1, angle2: The start and end angles for the pacman slice
        """
        if radius is None:
            radius = self.pacman_radius
            
            # Apply slight random variation to radius (±5%)
            radius_variation = self.rng.uniform(0.95, 1.05)
            radius *= radius_variation
        
        # Draw the pacman
        bbox = [x - radius, y - radius, x + radius, y + radius]
        self.draw.pieslice(bbox, angle1, angle2, fill=(0, 0, 0), outline=None)
        
        # Mark this position as taken
        grid_x = int(x // self.cell_size)
        grid_y = int(y // self.cell_size)
        self.taken_positions.add((grid_x, grid_y))
    
    def create_grid_pacmen(self):
        """Create a more organized grid of pacman shapes with slight variations"""
        for row in range(self.rows):
            for col in range(self.cols):
                # Skip if position is already taken by an emergent shape
                if (col, row) in self.taken_positions:
                    continue
                
                # 80% chance to place a pacman at each grid position
                # This creates a more complete but not perfectly uniform grid
                if self.rng.random() < 0.8:
                    # Add mild jitter to create slight irregularity
                    jitter_x = self.rng.randint(-self.grid_jitter, self.grid_jitter)
                    jitter_y = self.rng.randint(-self.grid_jitter, self.grid_jitter)
                    
                    x = col * self.cell_size + self.cell_size // 2 + jitter_x
                    y = row * self.cell_size + self.cell_size // 2 + jitter_y
                    
                    # Random angles for pacman mouth
                    # Use 90-degree increments with small variations for better readability
                    base_angle = self.rng.choice([0, 90, 180, 270])
                    variation = self.rng.randint(-15, 15)
                    start_angle = (base_angle + variation) % 360
                    
                    # Size of the "mouth" - consistent at around 90 degrees
                    mouth_size = 90 + self.rng.randint(-10, 10)
                    end_angle = (start_angle + 360 - mouth_size) % 360
                    
                    self.create_pacman(x, y, start_angle, end_angle)
    
    def create_kanizsa_triangle(self):
        """Create a Kanizsa triangle with slight irregularities"""
        for attempt in range(20):
            # Center point of the triangle
            center_x = self.rng.randint(self.width // 6, 5 * self.width // 6)
            center_y = self.rng.randint(self.height // 6, 5 * self.height // 6)
            
            # Size of the triangle (radius from center to corners)
            size = self.rng.randint(self.cell_size * 2, self.cell_size * 3)
            
            # Base rotation with some variation
            base_rotation = self.rng.randint(0, 360)
            
            # Triangle angles (approximately 120° apart with small variations)
            angle_variation = self.rng.randint(-5, 5)  # Reduced variation for better readability
            angle1 = base_rotation
            angle2 = (base_rotation + 120 + angle_variation) % 360
            angle3 = (base_rotation + 240 - angle_variation) % 360
            
            # Calculate corner positions
            corner1_x = center_x + size * math.cos(math.radians(angle1))
            corner1_y = center_y + size * math.sin(math.radians(angle1))
            corner2_x = center_x + size * math.cos(math.radians(angle2))
            corner2_y = center_y + size * math.sin(math.radians(angle2))
            corner3_x = center_x + size * math.cos(math.radians(angle3))
            corner3_y = center_y + size * math.sin(math.radians(angle3))
            
            # Check if all corners are within bounds
            padding = self.cell_size
            if (padding < corner1_x < self.width - padding and
                padding < corner1_y < self.height - padding and
                padding < corner2_x < self.width - padding and
                padding < corner2_y < self.height - padding and
                padding < corner3_x < self.width - padding and
                padding < corner3_y < self.height - padding):
                
                # Check if the positions are free
                grid_positions = [
                    (int(corner1_x // self.cell_size), int(corner1_y // self.cell_size)),
                    (int(corner2_x // self.cell_size), int(corner2_y // self.cell_size)),
                    (int(corner3_x // self.cell_size), int(corner3_y // self.cell_size))
                ]
                
                if any(pos in self.taken_positions for pos in grid_positions):
                    continue  # Try again if any position is taken
                
                # Create pacman at each corner with mouth facing inward
                # Use more consistent angles for better visibility
                
                # For corner 1, mouth points towards the triangle center
                angle_to_center1 = math.degrees(math.atan2(center_y - corner1_y, center_x - corner1_x))
                angle1_start = (angle_to_center1 - 45) % 360
                angle1_end = (angle_to_center1 + 45) % 360
                
                # For corner 2
                angle_to_center2 = math.degrees(math.atan2(center_y - corner2_y, center_x - corner2_x))
                angle2_start = (angle_to_center2 - 45) % 360
                angle2_end = (angle_to_center2 + 45) % 360
                
                # For corner 3
                angle_to_center3 = math.degrees(math.atan2(center_y - corner3_y, center_x - corner3_x))
                angle3_start = (angle_to_center3 - 45) % 360
                angle3_end = (angle_to_center3 + 45) % 360
                
                # Create the pacmen
                self.create_pacman(corner1_x, corner1_y, angle1_start, angle1_end)
                self.create_pacman(corner2_x, corner2_y, angle2_start, angle2_end)
                self.create_pacman(corner3_x, corner3_y, angle3_start, angle3_end)
                
                # Record this emergent shape
                self.emergent_shapes.append({
                    'type': 'triangle',
                    'corners': [(corner1_x, corner1_y), (corner2_x, corner2_y), (corner3_x, corner3_y)],
                    'size': size
                })
                
                return True
        
        return False  # Failed to place triangle after max attempts
    
    def create_kanizsa_rectangle(self):
        """Create a Kanizsa rectangle with better visibility"""
        for attempt in range(20):
            # Try to find a position for the rectangle
            grid_x = self.rng.randint(1, self.cols - 5)
            grid_y = self.rng.randint(1, self.rows - 5)
            
            # Rectangle dimensions (in grid cells)
            width_cells = self.rng.randint(2, 4)
            height_cells = self.rng.randint(2, 3)
            
            # Convert to pixel dimensions
            width = width_cells * self.cell_size
            height = height_cells * self.cell_size
            
            # Calculate corner positions (with less rotation for better visibility)
            rotation = self.rng.randint(-10, 10)  # Reduced rotation
            cos_rot = math.cos(math.radians(rotation))
            sin_rot = math.sin(math.radians(rotation))
            
            # Calculate corner positions
            start_x = grid_x * self.cell_size + self.cell_size // 2
            start_y = grid_y * self.cell_size + self.cell_size // 2
            
            # Corners relative to start position
            corners = [
                (0, 0),  # Top-left
                (width, 0),  # Top-right
                (width, height),  # Bottom-right
                (0, height)  # Bottom-left
            ]
            
            # Apply rotation and translation
            rotated_corners = []
            for x, y in corners:
                rx = start_x + (x * cos_rot - y * sin_rot)
                ry = start_y + (x * sin_rot + y * cos_rot)
                rotated_corners.append((rx, ry))
            
            # Check if all corners are within bounds
            padding = self.cell_size
            if all(padding < x < self.width - padding and padding < y < self.height - padding 
                   for x, y in rotated_corners):
                
                # Check if these positions are available
                grid_positions = [
                    (int(x // self.cell_size), int(y // self.cell_size))
                    for x, y in rotated_corners
                ]
                
                if any(pos in self.taken_positions for pos in grid_positions):
                    continue  # Try again if any position is taken
                
                # Calculate center of rectangle
                center_x = start_x + (width/2 * cos_rot - height/2 * sin_rot)
                center_y = start_y + (width/2 * sin_rot + height/2 * cos_rot)
                
                # Create pacmen at each corner with mouths pointing to create the illusory rectangle
                for x, y in rotated_corners:
                    # Angle from corner to center
                    angle_to_center = math.degrees(math.atan2(center_y - y, center_x - x))
                    
                    # Pacman mouth points toward center ±45°
                    angle1 = (angle_to_center - 45) % 360
                    angle2 = (angle_to_center + 45) % 360
                    
                    self.create_pacman(x, y, angle1, angle2)
                
                # Record this emergent shape
                self.emergent_shapes.append({
                    'type': 'rectangle',
                    'corners': rotated_corners,
                    'rotation': rotation,
                    'width': width,
                    'height': height
                })
                
                return True
        
        return False  # Failed to place rectangle after max attempts
    
    def create_largest_rectangle(self):
        """Create a significantly larger Kanizsa rectangle as the target shape to identify"""
        # Try multiple positions to find a good spot for the large rectangle
        for attempt in range(30):  # More attempts to ensure success
            # Position with some randomness but ensuring it fits
            grid_x = self.rng.randint(1, self.cols - 7)  # Leave more space for larger rectangle
            grid_y = self.rng.randint(1, self.rows - 7)
            
            # Make it larger than regular rectangles (5-7 cells wide, 4-6 cells tall)
            # We can make larger rectangles now that we have more grid space
            width_cells = self.rng.randint(5, 7)
            height_cells = self.rng.randint(4, 6)
            
            # Convert to pixel dimensions
            width = width_cells * self.cell_size
            height = height_cells * self.cell_size
            
            # Very slight rotation for better visibility
            rotation = self.rng.randint(-5, 5)
            cos_rot = math.cos(math.radians(rotation))
            sin_rot = math.sin(math.radians(rotation))
            
            # Calculate corner positions
            start_x = grid_x * self.cell_size + self.cell_size // 2
            start_y = grid_y * self.cell_size + self.cell_size // 2
            
            # Corners relative to start position
            corners = [
                (0, 0),  # Top-left
                (width, 0),  # Top-right
                (width, height),  # Bottom-right
                (0, height)  # Bottom-left
            ]
            
            # Apply rotation and translation
            rotated_corners = []
            for x, y in corners:
                rx = start_x + (x * cos_rot - y * sin_rot)
                ry = start_y + (x * sin_rot + y * cos_rot)
                rotated_corners.append((rx, ry))
            
            # Check if all corners are within bounds
            padding = self.cell_size
            if all(padding < x < self.width - padding and padding < y < self.height - padding 
                   for x, y in rotated_corners):
                
                # Check if these positions are available
                grid_positions = [
                    (int(x // self.cell_size), int(y // self.cell_size))
                    for x, y in rotated_corners
                ]
                
                if any(pos in self.taken_positions for pos in grid_positions):
                    continue  # Try again if any position is taken
                
                # Calculate center of rectangle
                center_x = start_x + (width/2 * cos_rot - height/2 * sin_rot)
                center_y = start_y + (width/2 * sin_rot + height/2 * cos_rot)
                
                # Create pacmen at each corner with mouths pointing to create the illusory rectangle
                for x, y in rotated_corners:
                    # Angle from corner to center
                    angle_to_center = math.degrees(math.atan2(center_y - y, center_x - x))
                    
                    # Pacman mouth points toward center ±45°
                    angle1 = (angle_to_center - 45) % 360
                    angle2 = (angle_to_center + 45) % 360
                    
                    self.create_pacman(x, y, angle1, angle2)
                
                # Record the corner grid positions as the expected response
                corner_grid_positions = []
                for x, y in rotated_corners:
                    grid_x = int(x // self.cell_size)
                    grid_y = int(y // self.cell_size)
                    corner_grid_positions.append((grid_x, grid_y))
                
                # Store this as the largest rectangle (with is_largest flag)
                self.emergent_shapes.append({
                    'type': 'rectangle',
                    'corners': rotated_corners,
                    'corner_grid_positions': corner_grid_positions,
                    'rotation': rotation,
                    'width': width,
                    'height': height,
                    'is_largest': True
                })
                
                return True
        
        return False  # Failed to place the large rectangle
    
    def create_multiple_shapes(self):
        """Create multiple Kanizsa shapes - both rectangles and triangles"""
        # Number of shapes to create (5-8 is a good range for visibility)
        num_shapes = self.rng.randint(5, 8)
        shapes_created = 0
        
        # Try to create at least 3 rectangles and 2 triangles
        min_rectangles = 3
        min_triangles = 2
        rectangles = 0
        triangles = 0
        
        while shapes_created < num_shapes and (shapes_created < 15):  # Added safety limit
            if rectangles < min_rectangles:
                if self.create_kanizsa_rectangle():
                    rectangles += 1
                    shapes_created += 1
            elif triangles < min_triangles:
                if self.create_kanizsa_triangle():
                    triangles += 1
                    shapes_created += 1
            else:
                # Once minimums are met, create random shapes
                if self.rng.random() < 0.5:
                    if self.create_kanizsa_rectangle():
                        rectangles += 1
                        shapes_created += 1
                else:
                    if self.create_kanizsa_triangle():
                        triangles += 1
                        shapes_created += 1
        
        # Set the expected count to the total number of shapes created
        self.expected_count = shapes_created
        return shapes_created
    
    def get_image_data_url(self):
        """Convert the image to a data URL for embedding in HTML"""
        buffer = io.BytesIO()
        self.image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}"
    
    def generate(self):
        """Generate a complete CAPTCHA with a largest rectangle challenge"""
        # First create the largest rectangle
        if not self.create_largest_rectangle():
            # If creation fails (very unlikely), try again with a different seed
            return generate_captcha(None)
        
        # Then create a few regular shapes as distractors
        num_distractors = self.rng.randint(3, 5)
        for _ in range(num_distractors):
            if self.rng.random() < 0.6:  # More rectangles than triangles for consistency
                self.create_kanizsa_rectangle()
            else:
                self.create_kanizsa_triangle()
        
        # Fill in the rest with grid-based pacmen
        self.create_grid_pacmen()
        
        # Add grid coordinates last so they're on top
        self.add_grid_coordinates()
        
        # Find the largest rectangle to get its corner coordinates
        largest_rectangle = next((s for s in self.emergent_shapes if s.get('is_largest')), None)
        corner_coords = []
        
        if largest_rectangle:
            # Extract the grid coordinates of the 4 corners
            corner_coords = largest_rectangle['corner_grid_positions']
        
        # Format as integers in clockwise order, starting from top-left
        # This gives us 4 integers for the challenge
        expected_answer = [coord for pos in corner_coords for coord in pos]
        
        return {
            'seed': self.seed,
            'expected_count': 4,  # Now we expect 4 corner coordinates
            'expected_answer': expected_answer,  # Store the actual coordinates
            'image_data': self.get_image_data_url(),
            'challenge_type': 'largest_rectangle'
        }

def generate_captcha(seed=None):
    """Helper function to generate a CAPTCHA"""
    captcha = GeometricCaptcha(seed=seed)
    return captcha.generate()

def regenerate_captcha(seed):
    """Regenerate a CAPTCHA with the same seed"""
    return generate_captcha(seed) 
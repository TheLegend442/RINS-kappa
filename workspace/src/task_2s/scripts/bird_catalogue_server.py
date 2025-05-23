#!/usr/bin/env python3

from task_2s.srv import BirdCollection
from task_2s.msg import Bird
import rclpy
from rclpy.node import Node

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle, Flowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle

from io import BytesIO
from PIL import Image as PILImage
import numpy as np

import cv2
from cv_bridge import CvBridge

bird_descriptions = {'laysan albatross': 'A large seabird known for long-distance flights, white with dark wingtips, breeding on remote Pacific islands.', 'yellow headed blackbird': 'A striking bird with bright yellow head and chest, black body, found in North American wetlands.', 'indigo bunting': 'Small songbird with vibrant blue plumage, common in woodlands and fields across eastern North America.', 'pelagic cormorant': 'A slender, dark seabird with a hooked bill, often found along rocky coasts and open ocean.', 'american crow': 'Common black bird, intelligent and adaptable, found throughout North America in diverse habitats.', 'yellow billed cuckoo': 'Medium-sized bird with slender body and yellow bill, inhabits woodlands and thickets in North America.', 'purple finch': 'Small finch with rosy-red plumage in males, commonly found in forests and suburban areas.', 'vermilion flycatcher': 'Bright red flycatcher with dark wings and tail, found in open habitats of the Americas.', 'european goldfinch': 'Small bird with red face, black and yellow wings, common in Europe and western Asia.', 'eared grebe': 'Diving waterbird with distinctive tufts near ears during breeding, found on freshwater lakes.', 'california gull': 'Medium gull with white and gray plumage, common along western North America coasts and inland lakes.', 'ruby throated hummingbird': 'Tiny hummingbird with iridescent green back and bright red throat in males, found in eastern North America.', 'blue jay': 'Vibrant blue bird with crest and loud calls, common in forests and suburban areas across eastern US.', 'pied kingfisher': 'Black and white kingfisher that hovers over water before diving for fish, found in Africa and Asia.', 'baltimore oriole': 'Bright orange and black songbird, common in eastern North America, known for hanging woven nests.', 'white pelican': 'Large white waterbird with long bill and throat pouch, found in inland lakes and marshes.', 'horned puffin': 'Seabird with colorful beak and small yellow “horns” above eyes, breeds on North Pacific cliffs.', 'white necked raven': 'Large raven with white neck feathers, inhabiting mountainous and forested regions in Africa.', 'great grey shrike': 'Predatory songbird with gray body and black mask, known for impaling prey on thorns.', 'house sparrow': 'Small, adaptable bird with brown and gray plumage, common worldwide in urban and rural areas.', 'cape glossy starling': 'Iridescent black starling with greenish and purplish sheen, native to southern Africa.', 'tree swallow': 'Small blue-green swallow with white belly, agile flyer, nests in tree cavities across North America.', 'common tern': 'Elegant seabird with slender body and forked tail, nests along coasts and inland waters worldwide.', 'red headed woodpecker': 'Striking woodpecker with bright red head and black-and-white body, found in open woodlands in North America.'}

def generate_catalogue(birds, filename="../bird_catalogue.pdf"):
    
    def convert_array_to_image_bytes(image_array, format="PNG"):
        """Convert a numpy image array to BytesIO buffer for ReportLab."""
        image = PILImage.fromarray(image_array.astype(np.uint8))
        buf = BytesIO()
        image.save(buf, format=format)
        buf.seek(0)
        return buf
    
    def add_background_image(canvas, doc, image_path="background.png"):
        """Add a background image to the PDF."""
        page_width, page_height = A4
        canvas.saveState()
        canvas.drawImage(image_path, 0, 0, width=page_width+1, height=page_height)
        canvas.restoreState()
    
    class OffsetParagraph(Flowable):
        def __init__(self, text, style, dx=0, dy=0):
            super().__init__()
            self.text = Paragraph(text, style)
            self.dx = dx
            self.dy = dy

        def wrap(self, availWidth, availHeight):
            return self.text.wrap(availWidth, availHeight)

        def draw(self):
            self.canv.saveState()
            self.canv.translate(self.dx, self.dy)
            self.text.drawOn(self.canv, 0, 0)
            self.canv.restoreState()
    
    
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    flowables = []
    
    pdfmetrics.registerFont(TTFont("Molle", "../bird_catalogue/fonts/Molle-Italic.ttf"))
    
    outline_style = ParagraphStyle(
        name="OutlineText",
        fontName="Molle",
        fontSize=40,
        leading=30, # line height
        alignment=1,
        textColor=colors.HexColor("#011c00")  # Shadow/border color
    )

    title_style = ParagraphStyle(
        name="TitleText",
        fontName="Molle",
        fontSize=40,
        leading=30, 
        alignment=1,
        # textColor=colors.HexColor("#2bb526"),  # Foreground color
        textColor = colors.HexColor("#22b01c")
    )

    # Now add to flowables
    flowables.append(OffsetParagraph("KAPPA Bird Catalogue", outline_style, dx=5, dy=-61))  # slightly offset
    flowables.append(Paragraph("KAPPA Bird Catalogue", title_style))  # main title
    flowables.append(Spacer(1, 1.5*cm))
    

    data = []
    row = []
    for i, bird in enumerate(birds):
        # Species above image
        styles['Heading3'].textColor = colors.HexColor("#011c00")
        species_para = Paragraph(f"<b>{bird.species}</b>", styles['Heading3'])

        # Image
        h, w = bird.image.shape[:2]
        height = h / w * 6 * cm
        image_buffer = convert_array_to_image_bytes(bird.image)
        bird_img = Image(image_buffer, width=6*cm, height=height)
        
        # Image Frame
        frameWidth = 5
        img_table = Table([[bird_img]], colWidths=[6*cm], rowHeights=[height])
        img_table.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), frameWidth, colors.HexColor("#9c703b")),  # border around the image
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        
        # Info below image
        info_text = (
            f"<b>Location:</b> {bird.location}<br/>"
            f"<b>Ring Color:</b> {bird.ring_color}<br/>"
            # f"<b>Detected:</b> {bird.detection_time}<br/>"
            f"<b>Description:</b> {bird.description}"
        )
        # styles['BodyText'].textColor = colors.HexColor("#082b07")
        styles['BodyText'].textColor = colors.HexColor("#011c00")
        info_para = Paragraph(info_text, styles['BodyText'])

        # Vertical stack of species, image, and info
        bird_block = [species_para, img_table, Spacer(1, 0.2*cm), info_para]
        bird_table = Table([[b] for b in bird_block], colWidths=[7.5*cm])

        row.append(bird_table)

        # Two birds per row
        if len(row) == 2:
            data.append(row)
            row = []

    # If there's an odd number of birds
    if row:
        row.append(Spacer(1, 0))  # empty cell for alignment
        data.append(row)

    # Create a table of all bird blocks
    grid = Table(data, colWidths=[7.5*cm, 7.5*cm])
    grid.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    flowables.append(grid)
    
    doc.build(
    flowables,
    onFirstPage=lambda c, d: add_background_image(c, d, image_path="../bird_catalogue/jungle_background_3.png"),
    onLaterPages=lambda c, d: add_background_image(c, d, image_path="../bird_catalogue/jungle_background_3.png")
    )

class Bird():
    def __init__(self, species, image, location, ring_color, detection_time, description):
        self.species = species
        self.image = image
        self.location = location
        self.ring_color = ring_color
        self.detection_time = detection_time
        self.description = description

class BirdCatalogueServer(Node):
    def __init__(self):
        super().__init__('bird_catalogue')
        self.srv = self.create_service(BirdCollection, 'bird_catalogue', self.bird_catalogue_callback)
        self.bird_list = []
        self.bridge = CvBridge()


    def bird_catalogue_callback(self, request, response):
        self.get_logger().info('Received request for bird catalogue')
        for bird in request.birds:
            bird_species = bird.species
            if "." in bird_species:
                bird_species = bird_species.split(".")[1]
            bird_species = bird_species.replace("_", " ")
            bird_species = bird_species.lower()


            cv_image = self.bridge.imgmsg_to_cv2(bird.image, desired_encoding='rgb8')
            new_bird = Bird(
                species=bird_species if bird_species in bird_descriptions else "Unknown",
                image=cv_image,
                location=bird.location,
                ring_color=bird.ring_color,
                detection_time=bird.detection_time,
                description=bird_descriptions[bird_species] if bird_species in bird_descriptions else "No description available"
            )
            self.bird_list.append(new_bird)
        self.get_logger().info(f'Added {len(request.birds)} birds to the catalogue')

        generate_catalogue(self.bird_list, filename="../bird_catalogue.pdf")

        return BirdCollection.Response()
    
def main(args=None):
    rclpy.init(args=args)
    node = BirdCatalogueServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
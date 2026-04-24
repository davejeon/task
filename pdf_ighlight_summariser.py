import pymupdf  # PyMuPDF

def extract_highlighted_text(pdf_path):
    doc = pymupdf.open(pdf_path)
    highlights = []
    
    for page_num, page in enumerate(doc, 1):
        annotations = page.annots()
        
        for annot in annotations:
            if annot.type[0] == 8:  # 8 = Highlight annotation
                # Get the quadpoints (coordinates of highlighted area)
                quad_points = annot.vertices
                
                if quad_points:
                    # Extract text within the highlighted region
                    highlighted_text = ""
                    for i in range(0, len(quad_points), 4):
                        quad = pymupdf.Quad(quad_points[i:i+4])
                        rect = quad.rect
                        text = page.get_text("text", clip=rect)
                        highlighted_text += text.strip()
                
                highlights.append({
                    "page": page_num,
                    "text": highlighted_text,
                    "color": annot.colors,
                    "date": annot.info.get("modDate", "N/A"),
                    "author": annot.info.get("title", "N/A"),
                })
    
    doc.close()
    return highlights


# --- Run it ---
pdf_path = "01_Deckblatt.pdf"  # update if needed
results = extract_highlighted_text(pdf_path)

if results:
    print(f"Found {len(results)} highlight(s):\n")
    for i, h in enumerate(results, 1):
        print(f"Highlight {i}:")
        print(f"  Page   : {h['page']}")
        print(f"  Text   : {h['text']}")
        print(f"  Color  : {h['color']}")
        print(f"  Date   : {h['date']}")
        print(f"  Author : {h['author']}")
        print()
else:
    print("No highlights found in the PDF.")

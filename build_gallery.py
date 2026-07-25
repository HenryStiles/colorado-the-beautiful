# build_gallery.py
import os
import re
import html
import openpyxl

# File paths
EXCEL_PATH = "/Users/henrys/source/colorado_the_beautiful/Outreach list.xlsx"
HTML_PATH = "/Users/henrys/source/colorado_the_beautiful/gallery.html"

def clean_slug(text):
    """Generates a clean ID slug from place name."""
    text = str(text).lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text

def build_card_html(row_idx, submitter, place_name, city, photo_url, story):
    """Generates the HTML card block for a single submission row."""
    slug = clean_slug(place_name) or f"item-{row_idx}"
    
    # Escape HTML to prevent injection and rendering issues
    submitter_esc = html.escape(str(submitter).strip())
    place_esc = html.escape(str(place_name).strip())
    city_esc = html.escape(str(city).strip())
    photo_url_esc = html.escape(str(photo_url).strip())
    story_esc = html.escape(str(story).strip().replace('\n', '<br>'))

    card = f"""
      <!-- Card: {place_esc} (by {submitter_esc}) -->
      <div class="card-container" id="landmark-{slug}" data-title="{place_esc}" data-submitter="{submitter_esc}" data-location="{city_esc}" data-photo="{photo_url_esc}" data-story="{story_esc}">
        <div class="card" role="button" tabindex="0" aria-expanded="false" aria-label="{place_esc}, click to enlarge details">
          <!-- Front Face -->
          <div class="card-front">
            <div class="card-image-wrapper">
              <img class="card-image" src="{photo_url_esc}" alt="{place_esc}">
            </div>
            <div class="card-overlay">
              <div class="card-location">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                </svg>
                {city_esc}
              </div>
              <h2 class="card-title">{place_esc}</h2>
              <div class="card-hint">
                <span>Read Story</span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>
          </div>
          <!-- Back Face -->
          <div class="card-back">
            <div class="card-back-header">
              <h2 class="card-back-title">{place_esc}</h2>
            </div>
            <p class="card-back-desc">"{story_esc}"</p>
            <div class="card-facts">
              <div class="fact-item">
                <span class="fact-label">Shared By</span>
                <span class="fact-value">{submitter_esc}</span>
              </div>
              <div class="fact-item">
                <span class="fact-label">Location</span>
                <span class="fact-value">{city_esc}</span>
              </div>
            </div>
            <button class="flip-back-btn" aria-label="Flip card to front">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
              Flip Back
            </button>
          </div>
        </div>
      </div>
"""
    return card

def main():
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: Excel file not found at {EXCEL_PATH}")
        return

    print(f"Loading submissions from {EXCEL_PATH}...")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    ws = wb['SUBMISSION Yeses']
    
    cards_html = []
    
    # Read rows skipping header
    for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        submitter = row[0]
        place_name = row[2]
        city = row[3]
        photo_url = row[4]
        story = row[5]
        
        # Check if row has valid data
        if not submitter or not place_name or not photo_url:
            continue
            
        print(f"  Row {idx}: Processing '{place_name}' by '{submitter}'...")
        card_html = build_card_html(idx, submitter, place_name, city, photo_url, story)
        cards_html.append(card_html)
        
    print(f"Generated {len(cards_html)} cards.")
    
    # Join card blocks
    new_cards_content = "\n".join(cards_html)
    
    # Read index.html
    if not os.path.exists(HTML_PATH):
        print(f"Error: index.html not found at {HTML_PATH}")
        return
        
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Replace content between placeholders
    start_tag = "<!-- CARDS_START -->"
    end_tag = "<!-- CARDS_END -->"
    
    pattern = re.compile(rf"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
    
    if not pattern.search(html_content):
        print("Error: Could not find <!-- CARDS_START --> and <!-- CARDS_END --> placeholders in index.html.")
        return
        
    replacement = f"{start_tag}\n{new_cards_content}\n      {end_tag}"
    updated_html = pattern.sub(replacement, html_content)
    
    # Save index.html
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(updated_html)
        
    print(f"Successfully updated {HTML_PATH}!")

if __name__ == "__main__":
    main()

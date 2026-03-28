"""
Oddschecker.com scraper using Playwright
Created: 2026
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import random
from datetime import datetime
from today_tomorrow import today_tomorrow1
from arbfunction import arb_opp, delete_arb
from booker import books


class OddsCheckerScraper:
    def __init__(self, new_urls, arb_urls, arb_opp_func, id_append, dont_add):
        print("OddsChecker Playwright Scraper initialized")
        self.new_urls = new_urls
        self.arb_urls = arb_urls
        self.arb_opp_func = arb_opp_func
        self.id_append = id_append
        self.dont_add = dont_add
        
    def scrape_odds(self, url):
        """Main scraping function using Playwright"""
        with sync_playwright() as p:
            # Launch browser with stealth settings
            browser = p.chromium.launch(
                headless=False,  # Set to True for production
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            
            # Create context with realistic settings
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
            )
            
            page = context.new_page()
            
            # Add random delay to appear more human
            time.sleep(random.uniform(2, 4))
            
            try:
                # Navigate to the page
                print(f"Navigating to: {url}")
                page.goto(url, wait_until='domcontentloaded', timeout=60000)
                
                # Wait for page to load
                time.sleep(random.uniform(1, 2))
                
                # Find all "All Odds" buttons
                all_odds_buttons = page.locator('a:has-text("All Odds")').all()
                print(f"\nFound {len(all_odds_buttons)} 'All Odds' buttons")
                
                # Process only the first match for testing
                for i, button in enumerate(all_odds_buttons[:1]):  # Only first match
                    try:
                        print(f"\n--- Processing match {i+1} ---")
                        
                        # Check if match is IN PLAY (skip if it is)
                        match_container = button.locator('xpath=ancestor::div[contains(@class, "match") or contains(@class, "event")]').first
                        in_play_badge = match_container.locator('text="IN PLAY"').count()
                        
                        if in_play_badge > 0:
                            print("Match is IN PLAY - skipping")
                            continue
                        
                        # Get match teams before clicking
                        teams_text = self.get_match_teams(button)
                        print(f"Match: {teams_text}")
                        
                        # Click the "All Odds" button
                        button.click()
                        print("Clicked 'All Odds' button")
                        
                        # Wait for odds page to load - wait for odds buttons to appear
                        try:
                            page.wait_for_selector('button[data-bk]', timeout=10000)
                            print("Odds buttons loaded")
                            time.sleep(random.uniform(1, 2))  # Extra wait for all odds to render
                        except:
                            print("Timeout waiting for odds buttons to load")
                            time.sleep(2)
                        
                        # Extract date
                        date_text = self.extract_date(page)
                        print(f"Date: {date_text}")
                        
                        # Check if date matches today or tomorrow
                        date1, date2 = today_tomorrow1()
                        if not self.date_matches(date_text, date1, date2):
                            print(f"Date doesn't match. Looking for {date1} or {date2}, found {date_text}")
                            page.go_back()
                            time.sleep(random.uniform(0.5, 1))
                            continue
                        
                        # Take screenshot for debugging
                        screenshot_path = 'c:/Users/JeffStone/Documents/foreign/arbs-beta1/odds_page_debug.png'
                        page.screenshot(path=screenshot_path)
                        print(f"Screenshot saved to: {screenshot_path}")
                        
                        # Print current URL
                        print(f"Current URL: {page.url}")
                        
                        # Extract odds data
                        odds_data = self.extract_odds(page)
                        
                        if odds_data:
                            print(f"\n✅ Found {len(odds_data)} odds entries")
                            
                            # Group by outcome
                            from collections import defaultdict
                            by_outcome = defaultdict(list)
                            for item in odds_data:
                                by_outcome[item['outcome']].append(f"{item['bookmaker']}: {item['odds']}")
                            
                            for outcome, odds_list in by_outcome.items():
                                print(f"\n{outcome}:")
                                for odd in odds_list:  # Show all bookmakers
                                    print(f"  {odd}")
                        else:
                            print("No odds data found")
                            
                            # Save HTML for inspection
                            html_path = 'c:/Users/JeffStone/Documents/foreign/arbs-beta1/odds_page_debug.html'
                            with open(html_path, 'w', encoding='utf-8') as f:
                                f.write(page.content())
                            print(f"HTML saved to: {html_path}")
                        
                        # Wait before closing so you can see the page
                        print("\nWaiting 5 seconds so you can see the page...")
                        time.sleep(5)
                        
                        # Don't go back for now, just close
                        print("Done with first match")
                        
                    except Exception as e:
                        print(f"Error processing match {i+1}: {e}")
                        try:
                            page.go_back()
                            time.sleep(random.uniform(0.5, 1))
                        except:
                            pass
                    
            except PlaywrightTimeout as e:
                print(f"Timeout error: {e}")
            except Exception as e:
                print(f"Error during scraping: {e}")
            finally:
                browser.close()
    
    def get_match_teams(self, all_odds_button):
        """Extract team names from the match row"""
        try:
            # Go up to parent container and find team names
            parent = all_odds_button.locator('xpath=ancestor::div[contains(@class, "match") or contains(@class, "event")]').first
            teams = parent.locator('text=/[A-Z][a-z]+/').all()
            
            if len(teams) >= 2:
                return f"{teams[0].text_content()} vs {teams[1].text_content()}"
            return "Unknown teams"
        except:
            return "Unknown teams"
    
    def extract_date(self, page):
        """Extract match date from the page"""
        date_selectors = [
            'time',  # Modern HTML5 time element
            '[class*="date"]',
            '[class*="Date"]',
            'span.date',
            'div.date',
            '#subevent-header time'
        ]
        
        for selector in date_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=2000):
                    date_text = element.text_content()
                    if date_text and date_text.strip():
                        print(f"Found date with selector '{selector}': {date_text}")
                        return date_text.strip()
            except:
                continue
        
        # Fallback to current date
        fallback_date = datetime.now().strftime("%A, %d %B")
        print(f"No date found, using fallback: {fallback_date}")
        return fallback_date
    
    def date_matches(self, page_date, date1, date2):
        """Check if page date matches today or tomorrow"""
        page_date_lower = page_date.lower()
        date1_lower = date1.lower()
        date2_lower = date2.lower()
        
        return (date1_lower in page_date_lower or 
                date2_lower in page_date_lower or
                'today' in page_date_lower or
                'tomorrow' in page_date_lower or
                any(day in page_date_lower for day in 
                    ['monday', 'tuesday', 'wednesday', 'thursday', 
                     'friday', 'saturday', 'sunday']))
    
    def extract_odds(self, page):
        """Extract betting odds from the page"""
        odds_data = []
        
        try:
            # Wait for the scrollable container to be present
            page.wait_for_selector('[id^="scrollable-container-"]', timeout=5000)
            
            # Get all odds area wrappers (one for each outcome: Home, Draw, Away)
            odds_areas = page.locator('div.oddsAreaWrapper_o17xb9rs').all()
            print(f"Found {len(odds_areas)} odds areas")
            
            for idx, odds_area in enumerate(odds_areas):
                try:
                    # Get the outcome heading - use index-based names since headings show "Odds"
                    outcome_names = ["Home Win", "Draw", "Away Win"]
                    outcome_name = outcome_names[idx] if idx < len(outcome_names) else f"Outcome {idx+1}"
                    print(f"Processing outcome: {outcome_name}")
                    
                    # Get all odds buttons for this outcome
                    odds_buttons = odds_area.locator('button[data-bk]').all()
                    print(f"  Found {len(odds_buttons)} odds buttons")
                    
                    for button in odds_buttons:
                        try:
                            bookmaker_code = button.get_attribute('data-bk')
                            odds_text = button.text_content().strip()
                            
                            if bookmaker_code and odds_text:
                                odds_data.append({
                                    'outcome': outcome_name,
                                    'bookmaker': bookmaker_code,
                                    'odds': odds_text
                                })
                        except Exception as e:
                            continue
                    
                except Exception as e:
                    print(f"Error processing odds area {idx}: {e}")
                    continue
            
        except Exception as e:
            print(f"Error extracting odds: {e}")
            import traceback
            traceback.print_exc()
        
        # If no data found, print page structure for debugging
        if not odds_data:
            print("\n=== DEBUG: No odds found, analyzing page structure ===")
            self.debug_page_structure(page)
        
        return odds_data
    
    def debug_page_structure(self, page):
        """Print page structure to help identify correct selectors"""
        try:
            # Check for betting odds container
            betting_container = page.locator('#betting-odds').first
            if betting_container.is_visible(timeout=2000):
                print("Found #betting-odds container")
                
                # Get all table rows
                all_rows = page.locator('tr').all()
                print(f"Total table rows on page: {len(all_rows)}")
                
                if all_rows:
                    # Print first row's HTML for inspection
                    first_row_html = all_rows[0].inner_html()
                    print(f"Sample row HTML (first 500 chars):")
                    print(first_row_html[:500])
            else:
                print("No #betting-odds container found")
                
            # Check for data attributes
            elements_with_data = page.locator('[data-bname], [data-best-dig], [data-best-bks]').all()
            print(f"Elements with data attributes: {len(elements_with_data)}")
            
        except Exception as e:
            print(f"Debug error: {e}")


def main():
    """Test the scraper"""
    scraper = OddsCheckerScraper(
        new_urls=[],
        arb_urls=[],
        arb_opp_func=arb_opp,
        id_append=[4, 5],
        dont_add=[]
    )
    
    # Test URL
    test_url = 'https://www.oddschecker.com/football/english/league-1'
    scraper.scrape_odds(test_url)


if __name__ == "__main__":
    main()

"""
Simplified summary extraction - creates tweet-level summaries
"""
import re
from typing import Dict, List, Any

def extract_simple_dates(text: str, deadlines: List[Dict[str, str]]) -> str:
    """Extract dates as single line: "10 Jun – 31 Jul 2026 (assets due 27 May)." """
    start_date = None
    end_date = None
    asset_deadline = None
    
    # Normalize text: replace various dash types with standard dash, normalize whitespace
    text_normalized = re.sub(r'[–—]', '-', text)  # Replace em/en dashes with hyphen
    text_normalized = re.sub(r'\s+', ' ', text_normalized)  # Normalize whitespace
    
    # First, try to extract from deadlines list
    for deadline in deadlines[:10]:  # Check more deadlines
        date_str = deadline.get('date', '')
        context = deadline.get('context', '').lower()
        
        # Normalize date string
        date_str = re.sub(r'[–—]', '-', date_str)
        
        # Check for date ranges (e.g., "10 June 2026 – 31 July 2026" or "10 June 2026 - 31 July 2026")
        if '–' in date_str or '-' in date_str:
            parts = re.split(r'[–-]', date_str, 1)
            if len(parts) == 2:
                if not start_date:
                    start_date = parts[0].strip()
                if not end_date:
                    end_date = parts[1].strip()
                continue
        
        # Check context for date types
        if 'start' in context or 'begin' in context or 'launch' in context or 'live' in context or 'campaign window' in context:
            if not start_date and date_str:
                start_date = date_str
        elif 'end' in context or 'finish' in context or 'conclusion' in context:
            if not end_date and date_str:
                end_date = date_str
        elif 'deadline' in context or 'deliver' in context or 'due' in context or 'asset' in context or 'delivery' in context:
            if not asset_deadline and date_str:
                asset_deadline = date_str
    
    # If we don't have dates from deadlines, try direct text extraction (using normalized text)
    if not start_date and not end_date:
        # Look for date range patterns like "10 June 2026 – 31 July 2026" or "10 June 2026 - 31 July 2026"
        # Support both hyphen and various dash types
        date_range_pattern = re.compile(
            r'\b(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\s*[–—-]\s*(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b',
            re.IGNORECASE
        )
        range_match = date_range_pattern.search(text_normalized[:3000])
        if range_match:
            start_date = range_match.group(1).strip()
            end_date = range_match.group(2).strip()
    
    # Also try to find asset deadline directly from text if not found (using normalized text)
    if not asset_deadline:
        asset_deadline_pattern = re.compile(
            r'(?:asset\s+delivery\s+deadline|assets\s+due|deliver.*?by|deadline.*?deliver).*?(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
            re.IGNORECASE | re.DOTALL
        )
        asset_match = asset_deadline_pattern.search(text_normalized[:3000])
        if asset_match:
            asset_deadline = asset_match.group(1).strip()
    
    # Format dates to shorter format (e.g., "10 Jun 2026" instead of "10 June 2026")
    def format_date_short(date_str: str) -> str:
        if not date_str:
            return date_str
        month_map = {
            'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr',
            'May': 'May', 'June': 'Jun', 'July': 'Jul', 'August': 'Aug',
            'September': 'Sep', 'October': 'Oct', 'November': 'Nov', 'December': 'Dec'
        }
        for full, short in month_map.items():
            date_str = date_str.replace(full, short).replace(full.lower(), short.lower())
        return date_str
    
    date_parts = []
    if start_date and end_date:
        date_parts.append(f"{format_date_short(start_date)} – {format_date_short(end_date)}")
    elif start_date:
        date_parts.append(format_date_short(start_date))
    elif end_date:
        date_parts.append(format_date_short(end_date))
    
    if asset_deadline:
        date_parts.append(f"(assets due {format_date_short(asset_deadline)})")
    
    return " ".join(date_parts) + "." if date_parts else "Dates not specified."


def extract_simple_channels(text: str) -> str:
    """Extract channels as single line: "Tesco website banners, Checkout ads, Instagram/Facebook Stories." """
    channels = []
    text_lower = text.lower()
    
    channel_map = {
        'Tesco website banners': ['website', 'onsite', 'site brand'],
        'Checkout ads': ['checkout'],
        'Instagram/Facebook Stories': ['instagram', 'facebook', 'stories'],
        'Display ads': ['display', 'banner'],
        'Email campaigns': ['email'],
    }
    
    for name, keywords in channel_map.items():
        if any(kw in text_lower for kw in keywords):
            channels.append(name)
            if len(channels) >= 4:
                break
    
    return ", ".join(channels) + "." if channels else "Channels not specified."


def extract_simple_kpis(text: str, kpis: Dict[str, List[float]]) -> str:
    """Extract KPIs as single line: "Targets: CTR ≥ 0.40%, add-to-basket ≥ 9%, +6% sales uplift." """
    parts = []
    text_lower = text.lower()
    
    priority = ['CTR', 'conversion_rate', 'sales_uplift', 'add-to-basket', 'ROAS']
    for kpi_name in priority:
        if kpi_name in kpis and kpis[kpi_name]:
            value = kpis[kpi_name][0]
            if kpi_name == 'CTR':
                parts.append(f"CTR ≥ {value}%")
            elif kpi_name == 'conversion_rate':
                parts.append(f"conversion ≥ {value}%")
            elif kpi_name == 'sales_uplift':
                parts.append(f"+{value}% sales uplift")
            elif kpi_name == 'add-to-basket':
                parts.append(f"add-to-basket ≥ {value}%")
            if len(parts) >= 3:
                break
    
    return "Targets: " + ", ".join(parts) + "." if parts else "Targets: Not specified."


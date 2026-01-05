"""
Structured extraction utilities for creating organized, deduplicated output
"""
import re
import logging
from typing import Dict, List, Any, Set

logger = logging.getLogger(__name__)


def deduplicate_list(items: List[str]) -> List[str]:
    """
    Remove duplicate items from a list (case-insensitive, normalized)
    
    Args:
        items: List of strings to deduplicate
        
    Returns:
        Deduplicated list preserving original case of first occurrence
    """
    seen: Set[str] = set()
    result = []
    for item in items:
        normalized = item.strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(item.strip())
    return result


def extract_goal(text: str) -> str:
    """
    Extract a short, tweet-level goal statement (2-3 lines max)
    
    Args:
        text: Document text
        
    Returns:
        One simple sentence describing the campaign/document goal
    """
    # Look for campaign launch/objective in first 1500 chars
    text_sample = text[:1500].lower()
    
    # Try to extract key action + product + retailer + objective
    goal_parts = []
    
    # Find product/brand name
    product_patterns = [
        r'launch\s+([A-Z][A-Za-z\s]+?)(?:\s+(?:at|in|on|via)|[.,;])',
        r'campaign\s+for\s+([A-Z][A-Za-z\s]+?)(?:\s+(?:at|in|on)|[.,;])',
        r'promote\s+([A-Z][A-Za-z\s]+?)(?:\s+(?:at|in|on)|[.,;])',
    ]
    
    product = None
    for pattern in product_patterns:
        match = re.search(pattern, text[:2000], re.IGNORECASE)
        if match:
            product = match.group(1).strip()
            # Limit product name length
            if len(product) > 50:
                words = product.split()
                product = ' '.join(words[:5])
            break
    
    # Find retailer/channel
    retailer_patterns = [r'at\s+([A-Z][A-Za-z]+)', r'via\s+([A-Z][A-Za-z]+)', r'([A-Z][A-Za-z]+)\s+website']
    retailer = None
    for pattern in retailer_patterns:
        match = re.search(pattern, text[:2000], re.IGNORECASE)
        if match:
            retailer = match.group(1).strip()
            break
    
    # Find objective
    objective_keywords = ['awareness', 'trial', 'sales', 'engagement', 'conversion']
    objective = None
    for keyword in objective_keywords:
        if keyword in text_sample:
            objective = keyword
            break
    
    # Build simple goal sentence
    if product and retailer:
        goal = f"Launch {product} at {retailer}"
        if objective:
            goal += f", building {objective}"
        # Add timing if available
        if 'summer' in text_sample or 'winter' in text_sample or 'spring' in text_sample or 'autumn' in text_sample:
            seasons = ['summer', 'winter', 'spring', 'autumn']
            for season in seasons:
                if season in text_sample:
                    goal += f" during {season}"
                    break
        goal += "."
    else:
        # Fallback: use first meaningful sentence (max 150 chars)
        sentences = re.split(r'[.!?]\s+', text)
        for sentence in sentences[:3]:
            sentence = sentence.strip()
            if len(sentence) > 30 and len(sentence) < 150:
                goal = sentence[:147] + ('...' if len(sentence) > 147 else '.')
                break
        else:
            goal = text[:147].strip() + ('...' if len(text) > 147 else '.')
    
    return goal


def extract_structured_dates(text: str, deadlines: List[Dict[str, str]]) -> List[str]:
    """
    Extract and format dates into structured list
    
    Args:
        text: Document text
        deadlines: List of deadline dictionaries from pattern matcher
        
    Returns:
        List of formatted date strings (e.g., "start: DD/MM/YYYY")
    """
    dates = []
    text_lower = text.lower()
    
    # Map deadline types
    for deadline in deadlines[:5]:  # Limit to 5 dates
        date_str = deadline.get('date', '')
        deadline_type = deadline.get('type', '')
        context = deadline.get('context', '').lower()
        
        # Determine date type from context
        if 'start' in context or 'begin' in context or 'launch' in context:
            date_type = 'start'
        elif 'end' in context or 'finish' in context or 'conclusion' in context:
            date_type = 'end'
        elif 'deadline' in context or 'deliver' in context or 'due' in context or 'submit' in context:
            date_type = 'asset_deadline'
        elif deadline_type == 'deadline':
            date_type = 'asset_deadline'
        else:
            # Check for other patterns
            if 'asset' in context:
                date_type = 'asset_deadline'
            else:
                date_type = None
        
        if date_type and date_str:
            dates.append(f"{date_type}: {date_str}")
    
    # If no dates found, try to find dates in text
    if not dates:
        date_pattern = re.compile(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b', re.IGNORECASE)
        found_dates = date_pattern.findall(text[:2000])
        if found_dates:
            dates.append(f"mentioned_date: {found_dates[0]}")
    
    return deduplicate_list(dates)


def extract_channels(text: str) -> List[str]:
    """
    Extract channel/placement information from document
    
    Args:
        text: Document text
        
    Returns:
        List of channel/placement names
    """
    channels = []
    text_lower = text.lower()
    
    # Common retail media channels
    channel_keywords = {
        'Tesco onsite brand formats': ['onsite brand', 'site brand', 'brand formats'],
        'Checkout placements': ['checkout', 'checkout double density', 'checkout single density'],
        'Social banners': ['social banner', 'social media banner', 'social ad'],
        'Display ads': ['display ad', 'display advertising', 'banner ad'],
        'Video ads': ['video ad', 'video creative', 'video format'],
        'Email campaigns': ['email campaign', 'email creative', 'email ad'],
        'In-store POS': ['point of sale', 'pos', 'in-store', 'in store display'],
        'Mobile ads': ['mobile ad', 'mobile banner', 'mobile creative'],
        'Desktop ads': ['desktop ad', 'desktop banner', 'desktop creative'],
    }
    
    for channel_name, keywords in channel_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            channels.append(channel_name)
    
    # Also look for explicit channel mentions
    channel_pattern = re.compile(r'(?:channel|placement|format)[\s:]+([A-Za-z\s]+(?:onsite|checkout|display|social|video|email|mobile|desktop)[A-Za-z\s]*)', re.IGNORECASE)
    matches = channel_pattern.findall(text[:3000])
    for match in matches:
        channel = match.strip()
        if len(channel) < 100 and channel not in channels:
            channels.append(channel)
    
    return deduplicate_list(channels)


def extract_primary_kpis(text: str, kpis: Dict[str, List[float]]) -> List[str]:
    """
    Extract primary KPIs as formatted strings
    
    Args:
        text: Document text
        kpis: KPI dictionary from pattern matcher
        
    Returns:
        List of formatted KPI strings
    """
    kpi_list = []
    
    # Format KPIs from dictionary
    kpi_formats = {
        'CTR': 'CTR target: {value}%',
        'conversion_rate': 'Conversion rate: {value}%',
        'CPC': 'CPC target: £{value}',
        'CPM': 'CPM target: £{value}',
        'ROAS': 'ROAS target: {value}',
        'CPA': 'CPA target: £{value}',
        'impressions': 'Impressions target: {value}',
        'clicks': 'Clicks target: {value}',
    }
    
    for kpi_name, values in kpis.items():
        if values:
            value = values[0]  # Take first value
            format_str = kpi_formats.get(kpi_name, '{kpi_name}: {value}')
            kpi_list.append(format_str.format(kpi_name=kpi_name.replace('_', ' ').title(), value=value))
    
    return deduplicate_list(kpi_list)


def extract_must_include(text: str, brand_guidelines: Dict[str, Any]) -> str:
    """
    Extract must-include elements as a single line
    
    Args:
        text: Document text
        brand_guidelines: Brand guidelines dictionary
        
    Returns:
        Single line string (e.g., "CrunchJoy logo + packshots (3 flavours max) + Tesco 'Only at Tesco' tag.")
    """
    elements = []
    text_lower = text.lower()
    
    # Find logo requirement
    if 'logo' in text_lower:
        # Try to find brand name
        brand_match = re.search(r'([A-Z][A-Za-z]+)\s+logo', text[:1000], re.IGNORECASE)
        if brand_match:
            elements.append(f"{brand_match.group(1)} logo")
        else:
            elements.append("logo")
    
    # Find packshot requirement
    if 'packshot' in text_lower:
        # Check for quantity limit
        quantity_match = re.search(r'(\d+)\s*(?:flavours?|variants?|products?)\s*(?:max|maximum)', text_lower)
        if quantity_match:
            elements.append(f"packshots ({quantity_match.group(1)} max)")
        else:
            elements.append("packshots")
    
    # Find tag requirement
    tag_patterns = [
        r"tesco['\s]+(?:tag|branding)",
        r"only at tesco",
        r"must include tesco",
    ]
    for pattern in tag_patterns:
        if re.search(pattern, text_lower):
            elements.append("Tesco 'Only at Tesco' tag")
            break
    
    if elements:
        result = " + ".join(elements) + "."
    else:
        result = "Required elements not specified."
    
    return result


def extract_biggest_donts(text: str, warnings: List[Dict[str, str]]) -> str:
    """
    Extract biggest 'don'ts' as a single line
    
    Args:
        text: Document text
        warnings: Warnings list from pattern matcher
        
    Returns:
        Single line string (e.g., "Don't mention prices, discounts, competitions, or health/sustainability claims.")
    """
    donts = []
    text_lower = text.lower()
    
    # Common don'ts
    dont_keywords = {
        'prices': ['no price', 'no pricing', 'avoid price', "don't mention price"],
        'discounts': ['no discount', 'no offer', 'avoid discount'],
        'competitions': ['no competition', 'no prize', 'no giveaway'],
        'health/sustainability claims': ['no health claim', 'no sustainability', 'no environmental claim'],
        'T&Cs': ['no t&cs', 'no terms and conditions'],
    }
    
    for dont_name, keywords in dont_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            donts.append(dont_name)
    
    # Limit to 4-5 items
    donts = donts[:4]
    
    if donts:
        result = "Don't mention " + ", ".join(donts) + "."
    else:
        result = "No specific restrictions specified."
    
    return result


def categorize_creative_requirements(
    technical_specs: Dict[str, Any],
    brand_guidelines: Dict[str, Any],
    text: str
) -> Dict[str, List[str]]:
    """
    Categorize creative requirements into must_have and optional
    
    Args:
        technical_specs: Technical specifications dict
        brand_guidelines: Brand guidelines dict
        text: Document text
        
    Returns:
        Dict with 'must_have' and 'optional' lists
    """
    must_have = []
    optional = []
    text_lower = text.lower()
    
    # Must-have: Logo, mandatory tags, required elements
    if 'logo' in text_lower or 'brand logo' in text_lower:
        must_have.append('Include brand logo')
    if 'tesco tag' in text_lower or 'must include tesco' in text_lower:
        must_have.append('Include Tesco tag/branding')
    if 'packshot' in text_lower:
        must_have.append('Include product packshot')
    if brand_guidelines.get('colors'):
        must_have.append('Use specified brand colors')
    if brand_guidelines.get('fonts'):
        must_have.append('Use specified fonts/typography')
    
    # Optional: Suggested elements
    if 'suggested' in text_lower or 'optional' in text_lower:
        optional.append('Consider optional elements as suggested in document')
    
    # Add formats as must-have
    if technical_specs.get('formats'):
        formats = ', '.join(technical_specs['formats'][:3])
        must_have.append(f'Use file formats: {formats}')
    
    return {
        'must_have': deduplicate_list(must_have),
        'optional': deduplicate_list(optional)
    }


def structure_technical_specs(technical_specs: Dict[str, Any], text: str) -> List[Dict[str, Any]]:
    """
    Structure technical specifications as array of placement objects
    
    Args:
        technical_specs: Technical specs dictionary
        text: Document text
        
    Returns:
        List of placement specification objects
    """
    placements = []
    text_lower = text.lower()
    
    # Extract dimensions
    dimensions = technical_specs.get('dimensions', [])
    formats = technical_specs.get('formats', [])
    
    # Try to match dimensions with placements
    placement_patterns = [
        (r'onsite[\s\w]*brand[\s\w]*desktop', 'Onsite Brand – Desktop'),
        (r'onsite[\s\w]*brand[\s\w]*mobile', 'Onsite Brand – Mobile'),
        (r'checkout[\s\w]*double[\s\w]*density', 'Checkout Double Density'),
        (r'checkout[\s\w]*single[\s\w]*density', 'Checkout Single Density'),
        (r'display[\s\w]*banner', 'Display Banner'),
        (r'social[\s\w]*banner', 'Social Banner'),
    ]
    
    # Create placements for each dimension
    for dim in dimensions[:5]:  # Limit to 5 placements
        placement_name = 'Creative Placement'
        # Try to find matching placement name
        for pattern, name in placement_patterns:
            if re.search(pattern, text_lower):
                placement_name = name
                break
        
        placement = {
            'placement': placement_name,
            'size': dim if 'x' in dim else f'{dim} px',
            'file_formats': formats[:3] if formats else ['JPG', 'PNG'],
            'min_font_size': '20 px',  # Default, can be enhanced
            'notes': []
        }
        
        # Add notes from text context
        if 'safe zone' in text_lower:
            placement['notes'].append('Respect safe zones')
        if 'cta' in text_lower and 'packshot' in text_lower:
            placement['notes'].append('Packshot must be closest to CTA')
        
        placements.append(placement)
    
    # If no dimensions, create a generic placement
    if not placements:
        placements.append({
            'placement': 'Standard Placement',
            'size': 'Various',
            'file_formats': formats[:3] if formats else ['JPG', 'PNG'],
            'min_font_size': '20 px',
            'notes': []
        })
    
    return placements


def categorize_guidelines(warnings: List[Dict[str, str]], text: str) -> Dict[str, List[str]]:
    """
    Categorize guidelines/warnings into rule categories
    
    Args:
        warnings: Warnings list from pattern matcher
        text: Document text
        
    Returns:
        Dict with categorized rule lists
    """
    text_lower = text.lower()
    
    copy_rules = []
    design_rules = []
    accessibility_rules = []
    legal_rules = []
    
    # Copy rules
    if 'no t&cs' in text_lower or 'no terms and conditions' in text_lower:
        copy_rules.append('No T&Cs allowed in creative.')
    if 'no competition' in text_lower or 'no prize draw' in text_lower:
        copy_rules.append('No competitions or charity messages.')
    if 'no sustainability claim' in text_lower:
        copy_rules.append('No sustainability claims if not allowed.')
    
    # Design rules
    if 'tesco tag' in text_lower and ('overlap' in text_lower or 'cover' in text_lower):
        design_rules.append('Nothing can overlap Tesco tags or value tiles.')
    if 'flat background' in text_lower or 'solid background' in text_lower:
        design_rules.append('Use flat background colour if specified.')
    
    # Accessibility rules
    if 'minimum font' in text_lower or 'font size' in text_lower:
        accessibility_rules.append('Respect minimum font sizes.')
    if 'contrast' in text_lower or 'wcag' in text_lower:
        accessibility_rules.append('Text and CTA must meet WCAG AA contrast.')
    
    # Legal rules
    if 'unverified claim' in text_lower or 'verified claim' in text_lower:
        legal_rules.append('No unverified claims or money-back guarantees.')
    if 'alcohol' in text_lower and ('requirement' in text_lower or 'guideline' in text_lower):
        legal_rules.append('Follow any alcohol-specific requirements if present.')
    
    # Add warnings to appropriate categories
    for warning in warnings:
        warning_text = warning.get('text', warning.get('message', '')).lower()
        if not warning_text:
            continue
        
        clean_warning = warning.get('text', warning.get('message', '')).strip()
        if not clean_warning:
            continue
        
        # Categorize based on content
        if any(word in warning_text for word in ['t&c', 'terms', 'condition', 'competition', 'charity', 'sustainability']):
            if clean_warning not in copy_rules:
                copy_rules.append(clean_warning[:150])
        elif any(word in warning_text for word in ['overlap', 'tag', 'tile', 'background', 'design', 'layout']):
            if clean_warning not in design_rules:
                design_rules.append(clean_warning[:150])
        elif any(word in warning_text for word in ['font', 'contrast', 'accessibility', 'wcag', 'readable']):
            if clean_warning not in accessibility_rules:
                accessibility_rules.append(clean_warning[:150])
        elif any(word in warning_text for word in ['legal', 'claim', 'guarantee', 'alcohol', 'regulatory', 'compliance']):
            if clean_warning not in legal_rules:
                legal_rules.append(clean_warning[:150])
        else:
            # Default to legal if can't categorize
            if clean_warning not in legal_rules:
                legal_rules.append(clean_warning[:150])
    
    return {
        'copy_rules': deduplicate_list(copy_rules),
        'design_rules': deduplicate_list(design_rules),
        'accessibility_rules': deduplicate_list(accessibility_rules),
        'legal_rules': deduplicate_list(legal_rules)
    }


def create_action_items(
    deadlines: List[Dict[str, str]],
    technical_specs: Dict[str, Any],
    warnings: List[Dict[str, str]],
    text: str
) -> List[str]:
    """
    Create imperative action items from extracted data (max 5 items, each ≤ 1 sentence)
    
    Args:
        deadlines: List of deadline dictionaries
        technical_specs: Technical specifications dict
        warnings: List of warning dictionaries
        text: Document text
        
    Returns:
        List of imperative action item strings (max 5)
    """
    action_items = []
    text_lower = text.lower()
    
    # Add deadline-based actions (limit 1)
    for deadline in deadlines[:1]:
        date_str = deadline.get('date', '')
        context = deadline.get('context', '').lower()
        if 'deliver' in context or 'deadline' in context or 'due' in context:
            action_items.append(f"Deliver final assets by {date_str}.")
            break
    
    # Add format requirements (limit 1)
    formats = technical_specs.get('formats', [])
    if formats:
        format_str = '/'.join(formats[:3])
        action_items.append(f"Use only {format_str} files in the required sizes.")
    
    # Add warning-based actions (limit 2)
    for warning in warnings[:2]:
        warning_text = warning.get('text', warning.get('message', ''))
        if warning_text:
            clean_text = warning_text.strip()[:100]  # Limit length
            if clean_text and len(clean_text) > 20:
                action_items.append(clean_text)
    
    # Add general requirements (limit 1)
    if 'tag' in text_lower and 'tesco' in text_lower:
        action_items.append("Include required tags/value tiles as specified.")
    elif 't&c' in text_lower or 'terms and conditions' in text_lower:
        action_items.append("Avoid any T&Cs, competition, or sustainability text in creative.")
    
    return deduplicate_list(action_items)[:5]  # Limit to 5 items


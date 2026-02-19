"""
Industry-Specific Analysis Rules
Different evaluation criteria for different industries
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class IndustryProfile:
    """Industry-specific financial characteristics"""
    name: str
    typical_margins: str
    typical_leverage: str
    leverage_is_good: bool  # Whether high leverage is normal/acceptable
    leverage_reason: str
    key_metrics: List[str]
    warning_thresholds: Dict[str, float]
    evaluation_notes: str


# Industry profiles
INDUSTRY_PROFILES = {
    'Defense': IndustryProfile(
        name='Defense Contractors',
        typical_margins='Low-to-moderate (8-12%) - fixed government contracts',
        typical_leverage='High (D/E 2-4x) - normal for industry',
        leverage_is_good=True,
        leverage_reason='Stable long-term government contracts + predictable cash flows make high leverage safe and necessary to boost ROE given fixed margins',
        key_metrics=['Contract backlog', 'Government revenue %', 'Debt maturity profile'],
        warning_thresholds={
            'debt_to_equity': 5.0,  # Higher threshold for defense
            'current_ratio': 1.0,
        },
        evaluation_notes='''
Defense contractors operate under unique conditions:
1. Fixed-price government contracts limit margin expansion
2. Long-term contracts (5-10 years) provide predictable cash flows
3. High leverage is STRATEGIC - used to boost ROE since margins are capped
4. Debt is SAFE because government is reliable counterparty
5. Stock buybacks are common to further reduce equity and boost ROE

Financial metrics that look "dangerous" in other industries are NORMAL here:
- D/E of 3.0x+ is typical (LMT: 3.4x is within range)
- ROE > 50% is common (leverage-driven but sustainable)
- ROA of 7-10% is actually good for fixed-margin business

Key evaluation factors:
- Contract backlog visibility
- Government revenue concentration
- Political risk (budget changes)
- Debt maturity schedule (not just total debt)
'''
    ),
    
    'Technology': IndustryProfile(
        name='Technology',
        typical_margins='High (20-40%)',
        typical_leverage='Low (D/E < 0.5x)',
        leverage_is_good=False,
        leverage_reason='Tech companies should fund growth through operations, not debt',
        key_metrics=['R&D spend', 'Revenue growth', 'Margin expansion'],
        warning_thresholds={
            'debt_to_equity': 1.0,
            'current_ratio': 1.5,
        },
        evaluation_notes='High leverage in tech is a red flag'
    ),
    
    'Utilities': IndustryProfile(
        name='Utilities',
        typical_margins='Moderate (15-25%)',
        typical_leverage='High (D/E 1.5-3x)',
        leverage_is_good=True,
        leverage_reason='Stable regulated business with predictable cash flows',
        key_metrics=['Regulated return', 'Dividend coverage', 'Rate base growth'],
        warning_thresholds={
            'debt_to_equity': 4.0,
            'current_ratio': 0.8,
        },
        evaluation_notes='Like defense, utilities use leverage strategically'
    ),
    
    'REITs': IndustryProfile(
        name='Real Estate Investment Trusts',
        typical_margins='High (50-70% gross)',
        typical_leverage='High (Debt/Assets 40-60%)',
        leverage_is_good=True,
        leverage_reason='Real estate is inherently leveraged; stable rental income services debt',
        key_metrics=['FFO', 'Occupancy', 'Debt maturity'],
        warning_thresholds={
            'debt_to_equity': 6.0,
            'current_ratio': 0.5,
        },
        evaluation_notes='REITs are designed to use leverage; look at interest coverage'
    ),
    
    'Banks': IndustryProfile(
        name='Banking & Financials',
        typical_margins='Moderate (20-30% net interest)',
        typical_leverage='Very High (10-20x assets/equity)',
        leverage_is_good=True,
        leverage_reason='Banking IS leverage - they borrow short and lend long',
        key_metrics=['NIM', 'Capital ratios', 'NPL ratio'],
        warning_thresholds={
            'debt_to_equity': 15.0,
            'current_ratio': 1.0,
        },
        evaluation_notes='Use Tier 1 capital ratio, not D/E. High leverage is business model.'
    ),
}


def get_industry_profile(sector: str, industry: str = "") -> Optional[IndustryProfile]:
    """Get industry profile based on sector/industry"""
    
    # Defense/Aerospace detection
    defense_keywords = ['defense', 'aerospace', 'military', 'weapons', 'government services']
    if any(kw in sector.lower() or kw in industry.lower() for kw in defense_keywords):
        return INDUSTRY_PROFILES['Defense']
    
    # Technology
    tech_keywords = ['technology', 'software', 'internet', 'semiconductor']
    if any(kw in sector.lower() for kw in tech_keywords):
        return INDUSTRY_PROFILES['Technology']
    
    # Utilities
    utility_keywords = ['utilities', 'electric', 'gas', 'water']
    if any(kw in sector.lower() for kw in utility_keywords):
        return INDUSTRY_PROFILES['Utilities']
    
    # REITs
    if 'reit' in sector.lower() or 'real estate' in sector.lower():
        return INDUSTRY_PROFILES['REITs']
    
    # Banks
    bank_keywords = ['banks', 'financial services', 'insurance']
    if any(kw in sector.lower() for kw in bank_keywords):
        return INDUSTRY_PROFILES['Banks']
    
    return None


def evaluate_leverage_in_context(debt_to_equity: float, sector: str, industry: str = "") -> Dict:
    """Evaluate leverage in industry context"""
    
    profile = get_industry_profile(sector, industry)
    
    if not profile:
        # Standard evaluation
        return {
            'is_concerning': debt_to_equity > 1.5,
            'context': 'Standard industry',
            'threshold': 1.5,
            'explanation': f'D/E of {debt_to_equity:.2f}x is {"high" if debt_to_equity > 1.5 else "acceptable"}'
        }
    
    # Industry-specific evaluation
    threshold = profile.warning_thresholds.get('debt_to_equity', 1.5)
    is_high = debt_to_equity > threshold
    
    if profile.leverage_is_good and not is_high:
        # Below industry norm - might be under-leveraged
        return {
            'is_concerning': False,
            'is_opportunity': debt_to_equity < threshold * 0.6,
            'context': profile.name,
            'threshold': threshold,
            'explanation': f'D/E of {debt_to_equity:.2f}x is {"below" if debt_to_equity < threshold * 0.8 else "within"} industry norm ({profile.typical_leverage})',
            'note': profile.leverage_reason
        }
    elif profile.leverage_is_good and is_high:
        # High but acceptable in context
        is_dangerous = debt_to_equity > threshold * 1.3
        return {
            'is_concerning': is_dangerous,
            'context': profile.name,
            'threshold': threshold,
            'explanation': f'D/E of {debt_to_equity:.2f}x is {"within" if not is_dangerous else "above"} acceptable range for {profile.name}',
            'note': profile.leverage_reason if not is_dangerous else f'Warning: Even for {profile.name}, this is high'
        }
    else:
        # Standard concern
        return {
            'is_concerning': is_high,
            'context': profile.name,
            'threshold': threshold,
            'explanation': f'D/E of {debt_to_equity:.2f}x is {"high" if is_high else "acceptable"} for {profile.name}'
        }


def evaluate_roe_in_context(roe: float, roa: float, debt_to_equity: float, 
                            sector: str, industry: str = "") -> Dict:
    """Evaluate ROE in industry context"""
    
    profile = get_industry_profile(sector, industry)
    
    if not profile:
        # Standard evaluation
        if roa and roa > 0:
            leverage_ratio = roe / roa
            is_leverage_driven = leverage_ratio > 5
            return {
                'is_quality': not is_leverage_driven,
                'leverage_ratio': leverage_ratio,
                'explanation': f'ROE/ROA = {leverage_ratio:.1f}x ({"leverage-driven" if is_leverage_driven else "quality"})'
            }
        return {'is_quality': True, 'explanation': 'Cannot evaluate without ROA'}
    
    # Industry-specific ROE evaluation
    if profile.leverage_is_good:
        # For industries where leverage is normal
        leverage_ratio = roe / roa if (roa and roa > 0) else 0
        
        if roe > 50 and leverage_ratio > 8:
            # High ROE from leverage - but expected in this industry
            return {
                'is_quality': True,  # In context, this is normal
                'is_leverage_driven': True,
                'leverage_ratio': leverage_ratio,
                'explanation': f'ROE {roe:.1f}% is leverage-driven (ROA {roa:.1f}%), which is NORMAL for {profile.name}',
                'context_note': profile.leverage_reason,
                'warning': None  # No warning needed - this is industry norm
            }
        elif roe < 20:
            # Low ROE for a leverage-friendly industry
            return {
                'is_quality': False,
                'explanation': f'ROE {roe:.1f}% is low for {profile.name} where leverage should boost returns',
                'context_note': 'May indicate poor contract backlog or operational issues'
            }
    
    # Standard evaluation
    return {
        'is_quality': True,
        'explanation': f'ROE {roe:.1f}% for {profile.name}'
    }


def format_industry_context(sector: str, industry: str = "") -> str:
    """Format industry context for display"""
    profile = get_industry_profile(sector, industry)
    
    if not profile:
        return ""
    
    lines = []
    lines.append(f"\n🏭 行业特征分析 ({profile.name}):")
    lines.append("-" * 50)
    lines.append(f"  典型利润率: {profile.typical_margins}")
    lines.append(f"  典型杠杆率: {profile.typical_leverage}")
    lines.append("")
    lines.append(f"  💡 行业洞察:")
    for line in profile.evaluation_notes.strip().split('\n'):
        if line.strip():
            lines.append(f"    {line}")
    lines.append("-" * 50)
    
    return "\n".join(lines)


# Test
if __name__ == "__main__":
    # Test with LMT
    print("Testing LMT (Defense):")
    result = evaluate_leverage_in_context(3.4, "Industrials", "Defense")
    print(f"  D/E 3.4x: {result}")
    
    roe_result = evaluate_roe_in_context(76.9, 7.6, 3.4, "Industrials", "Defense")
    print(f"  ROE 76.9%: {roe_result}")
    
    print("\n" + format_industry_context("Industrials", "Defense"))

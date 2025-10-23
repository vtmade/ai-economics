"""
Goods Market Implementation

Implements product market with:
- Price adjustment based on supply and demand
- Market clearing
- Demand from workers (consumption) and firms (investment)
"""

import numpy as np
from typing import Dict


class GoodsMarket:
    """
    Goods market with price adjustment mechanism.

    Implements a simple market clearing process where prices
    adjust based on excess demand.
    """

    def __init__(self, model, config: Dict):
        """
        Initialize goods market.

        Args:
            model: Mesa model instance
            config: Market configuration
        """
        self.model = model
        self.config = config

        self.price = config.get('initial_price', 100)
        self.price_adjustment_speed = config.get('price_adjustment_speed', 0.15)
        self.demand_elasticity = config.get('demand_elasticity', 1.2)

        # Market quantities
        self.total_supply = 0
        self.total_demand = 0
        self.total_sales = 0

        # History
        self.price_history = []
        self.supply_history = []
        self.demand_history = []

    def clear_market(self):
        """
        Clear the market by adjusting prices based on supply and demand.
        """
        # Calculate total supply (sum of firm production)
        firms = [agent for agent in self.model.schedule.agents
                if hasattr(agent, 'production')]
        self.total_supply = sum(f.production for f in firms)

        # Calculate total demand
        self.total_demand = self._calculate_total_demand()

        # Adjust price based on excess demand
        if self.total_supply > 0:
            excess_demand = (self.total_demand - self.total_supply) / self.total_supply

            # Price adjustment
            price_change = self.price_adjustment_speed * excess_demand
            self.price *= (1 + price_change)

            # Keep price positive and reasonable
            self.price = max(self.price, 10)
            self.price = min(self.price, 1000)

        # Calculate sales (min of supply and demand)
        self.total_sales = min(self.total_supply, self.total_demand)

        # Record history
        self.price_history.append(self.price)
        self.supply_history.append(self.total_supply)
        self.demand_history.append(self.total_demand)

    def _calculate_total_demand(self) -> float:
        """
        Calculate total demand for goods.

        Demand comes from:
        1. Worker consumption
        2. Firm investment demand
        3. Government spending

        Returns:
            float: Total demand
        """
        total_demand = 0

        # Worker consumption demand
        workers = [agent for agent in self.model.schedule.agents
                  if hasattr(agent, 'consumption')]

        # Consumption demand is in currency, convert to real demand
        consumption_demand = sum(w.consumption for w in workers)
        real_consumption_demand = consumption_demand / self.price

        # Price elasticity of demand
        real_consumption_demand *= (100 / self.price) ** (self.demand_elasticity - 1)

        total_demand += real_consumption_demand

        # Firm investment demand (firms buying capital goods)
        firms = [agent for agent in self.model.schedule.agents
                if hasattr(agent, 'profits')]

        investment_demand = sum(f.profits * f.investment_rate for f in firms if f.profits > 0)
        real_investment_demand = investment_demand / self.price

        total_demand += real_investment_demand

        return total_demand

    def get_price(self) -> float:
        """Get current market price."""
        return self.price

    def get_statistics(self) -> Dict:
        """
        Get goods market statistics.

        Returns:
            Dict: Market statistics
        """
        return {
            'price': self.price,
            'total_supply': self.total_supply,
            'total_demand': self.total_demand,
            'total_sales': self.total_sales,
            'excess_demand': self.total_demand - self.total_supply
        }

    def calculate_gdp(self) -> float:
        """
        Calculate GDP (total production value).

        Returns:
            float: GDP
        """
        return self.total_sales * self.price

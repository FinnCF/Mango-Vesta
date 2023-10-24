risk_ranking_parameters = {
    'AAA': {
        'Init Ass / Liab': (1, 1),
        'Main Ass / Liab': (1, 1),
        'Borrow Fee (%)': 0.05,
        'Borrow Upkeep Rate (%)': 0.50,
        'Liq Fee (%)': 0,
        'Insured?': 'Y',
        'Deposit / Borrow Scaling Start ($)': float('inf'),
        'Net Borrow Limit ($)': float('inf')
    },
    'AA': {
        'Init Ass / Liab': (0.95, 1.05),
        'Main Ass / Liab': (0.95, 1.05),
        'Borrow Fee (%)': 0.075,
        'Borrow Upkeep Rate (%)': 0.75,
        'Liq Fee (%)': 2.5,
        'Insured?': 'Y',
        'Deposit / Borrow Scaling Start ($)': 10_000_000,
        'Net Borrow Limit ($)': 10_000_000
    },
    'A': {
        'Init Ass / Liab': (0.9, 1.1),
        'Main Ass / Liab': (0.9, 1.1),
        'Borrow Fee (%)': 0.1,
        'Borrow Upkeep Rate (%)': 1,
        'Liq Fee (%)': 3,
        'Insured?': 'Y',
        'Deposit / Borrow Scaling Start ($)': 5_000_000,
        'Net Borrow Limit ($)': 5_000_000
    },
    'BBB': {
        'Init Ass / Liab': (0.85, 1.15),
        'Main Ass / Liab': (0.85, 1.15),
        'Borrow Fee (%)': 0.125,
        'Borrow Upkeep Rate (%)': 1.25,
        'Liq Fee (%)': 7.5,
        'Insured?': 'Y',
        'Deposit / Borrow Scaling Start ($)': 100_000,
        'Net Borrow Limit ($)': 100_000
    },
    'BB': {
        'Init Ass / Liab': (0.7, 1.3),
        'Main Ass / Liab': (0.7, 1.3),
        'Borrow Fee (%)': 0.15,
        'Borrow Upkeep Rate (%)': 1.5,
        'Liq Fee (%)': 10,
        'Insured?': 'Y',
        'Deposit / Borrow Scaling Start ($)': 50_000,
        'Net Borrow Limit ($)': 50_000
    },
    'B': {
        'Init Ass / Liab': (0.55, 1.45),
        'Main Ass / Liab': (0.55, 1.45),
        'Borrow Fee (%)': 0.2,
        'Borrow Upkeep Rate (%)': 2,
        'Liq Fee (%)': 12.5,
        'Insured?': 'Y',
        'Deposit / Borrow Scaling Start ($)': 35_000,
        'Net Borrow Limit ($)': 35_000
    },
    'CCC': {
        'Init Ass / Liab': (0.5, 1.5),
        'Main Ass / Liab': (0.5, 1.5),
        'Borrow Fee (%)': 0.25,
        'Borrow Upkeep Rate (%)': 2.5,
        'Liq Fee (%)': 15,
        'Insured?': 'N',
        'Deposit / Borrow Scaling Start ($)': 25_000,
        'Net Borrow Limit ($)': 25_000
    },
    'CC': {
        'Init Ass / Liab': (0.3, 1.7),
        'Main Ass / Liab': (0.3, 1.7),
        'Borrow Fee (%)': 0.35,
        'Borrow Upkeep Rate (%)': 4,
        'Liq Fee (%)': 20,
        'Insured?': 'N',
        'Deposit / Borrow Scaling Start ($)': 15_000,
        'Net Borrow Limit ($)': 15_000
    },
    'C': {
        'Init Ass / Liab': (0.1, 1.9),
        'Main Ass / Liab': (0.1, 1.9),
        'Borrow Fee (%)': 0.5,
        'Borrow Upkeep Rate (%)': 5,
        'Liq Fee (%)': 30,
        'Insured?': 'N',
        'Deposit / Borrow Scaling Start ($)': 5_000,
        'Net Borrow Limit ($)': 5_000
    },
    'D': {
        'Init Ass / Liab': (0, 2),
        'Main Ass / Liab': (0, 2),
        'Borrow Fee (%)': 1,
        'Borrow Upkeep Rate (%)': 10,
        'Liq Fee (%)': 40,
        'Insured?': 'N',
        'Deposit / Borrow Scaling Start ($)': 2_500,
        'Net Borrow Limit ($)': 2_500
    }
}

def calculate_total(prices):
    total = 0
    # Плохой код: использование eval и хардкод
    for p in prices:
        total = total + eval(str(p))
    return total

# Захардкоженный токен (плохая практика)
API_TOKEN = "12345-secret-token"
print(calculate_total([10, 20, 30]))

import os
import subprocess
from anthropic import Anthropic

def get_git_diff():
    """Получает diff изменений между ветками."""
    try:
        result = subprocess.run(
            ["git", "diff", "origin/main...HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        print(f"Ошибка при получении git diff: {e}")
        return ""

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ОШИБКА: Переменная ANTHROPIC_API_KEY не найдена в окружении!")
        with open("review_comment.md", "w", encoding="utf-8") as f:
            f.write("⚠️ Ошибка авторизации: API key не найден в secrets.")
        return

    diff = get_git_diff()
    
    if not diff.strip():
        print("Изменений не найдено.")
        with open("review_comment.md", "w", encoding="utf-8") as f:
            f.write("Проверено: изменений в коде не обнаружено.")
        return

    client = Anthropic(api_key=api_key)

    system_prompt = """
    Ты — Senior Software Engineer. Проведи ревью кода из git diff.
    Найди потенциальные баги, проблемы с безопасностью или стилем.
    Формат ответа:
    1. Краткая выжимка изменений.
    2. Замечания (если есть) с указанием файла и строки.
    3. Итоговый вердикт: 🟢 APPROVE или 🔴 NEEDS CHANGES.
    """

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": f"Сделай ревью diff:\n\n```diff\n{diff}\n```"}]
    )

    review = response.content[0].text

    with open("review_comment.md", "w", encoding="utf-8") as f:
        f.write(review)

if __name__ == "__main__":
    main()

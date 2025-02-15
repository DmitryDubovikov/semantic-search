from faker import Faker

from .schemas import NewsItem

fake = Faker("en_US")


def generate_news_fixtures(num_items: int = 10) -> list[NewsItem]:
    fixtures = []
    for _ in range(num_items):

        topic = fake.random_element(elements=("AI", "Space Exploration", "Renewable Energy", "Healthcare", "Finance"))

        title = f"Breakthrough in {topic}: {fake.sentence(nb_words=4)}"
        content = f"Recent developments in {topic} have led to {fake.paragraph(nb_sentences=5)}"
        fixtures.append(NewsItem(title=title, content=content))
    return fixtures

from typing import Optional
from beanie import Document, Link
from .user import User


def get_questions_list() -> list[str]:
    questions = [
        "Beauty - convenience - quality (prioritize)",
        "Describe your favorite thing",
        "Do you like shopping?",
        "Shopping style - how do you do it? Favorite stores?",
        "What is the order (clutter) in the wardrobe?",
        "How much care does the clothing require? Do you like to take care of your clothes?",
        "Favorite color? Textile?",
        "Prints in your wardrobe - what and how many of them?",
        "Jewelry in your wardrobe - what and how many of them?",
        "Makeup - what do you usually do?",
        "Do you have a lot of shoes and do you wear heels?",
        "How often do you change your hairstyles and hair color?",
        "Are you so comfortable or does this outfit depend on the circumstances?",
        "Are you a fan of noisy parties, holidays, or social events? If you need to go, how will you behave?",
        "What is your dream car?",
        "How did you study at school? What sports sections did you attend and why?",
        "What do you do? Is there a dress code? Do you like this job?",
        "What impression do you want to make?",
        "What is your lifestyle or schedule (business trips, receptions, lots of sports, travel, nightlife)?"
    ]
    return questions


class PsychoType(Document):
    user: Link[User]

    # 1. Beauty – convenience – quality (prioritize)
    beauty_convenience_quality: Optional[str] = ""

    # 2. Describe your favorite thing
    favorite_thing: Optional[str] = ""

    # 3. Do you like shopping?
    like_shopping: Optional[str] = ""

    # 4. Shopping style - how do you do it? Favorite stores?
    shopping_style: Optional[str] = ""

    # 5. What is the order (clutter) in the wardrobe?
    wardrobe_order: Optional[str] = ""

    # 6. How much care does the clothing require? Do you like to take care of your clothes?
    clothing_care: Optional[str] = ""

    # 7. Favorite color? Textile?
    favorite_color_textile: Optional[str] = ""

    # 8. Prints in your wardrobe - what and how many of them?
    wardrobe_prints: Optional[str] = ""

    # 9. Jewelry in your wardrobe – what and how many of them?
    wardrobe_jewelry: Optional[str] = ""

    # 10. Makeup – what do you usually do?
    makeup_routine: Optional[str] = ""

    # 11. Do you have a lot of shoes and do you wear heels?
    shoe_collection: Optional[str] = ""

    # 12. How often do you change your hairstyles and hair color?
    hairstyle_frequency: Optional[str] = ""

    # 13. Are you so comfortable or does this outfit depend on the circumstances?
    outfit_comfort: Optional[str] = ""

    # 14. Are you a fan of noisy parties, holidays, or social events? If you need to go, how will you behave?
    social_event_preference: Optional[str] = ""

    # 15. What is your dream car?
    dream_car: Optional[str] = ""

    # 16. How did you study at school? What sports sections did you attend and why?
    school_performance: Optional[str] = ""

    # 17. What do you do? Is there a dress code? Do you like this job?
    profession: Optional[str] = ""

    # 18. What impression do you want to make?
    desired_impression: Optional[str] = ""

    # 19. What is your lifestyle or schedule (business trips, receptions, lots of sports, travel, nightlife)?
    lifestyle_schedule: Optional[str] = ""

    def to_string(self) -> str:
        values = [v for v in self.model_dump().values()]
        zipped_list = zip(get_questions_list(), values)
        return "\n".join([f"question:{item[0]}\nanswer:{item[1]}" for item in zipped_list])

from mongoengine import *

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


class PsychoType(Document):
    # 1. Beauty – convenience – quality (prioritize)
    beauty_convenience_quality = StringField()

    # 2. Describe your favorite thing
    favorite_thing = StringField()

    # 3. Do you like shopping?
    like_shopping = StringField()

    # 4. Shopping style - how do you do it? Favorite stores?
    shopping_style = StringField()

    # 5. What is the order (clutter) in the wardrobe?
    wardrobe_order = StringField()

    # 6. How much care does the clothing require? Do you like to take care of your clothes?
    clothing_care = StringField()

    # 7. Favorite color? Textile?
    favorite_color_textile = StringField()

    # 8. Prints in your wardrobe - what and how many of them?
    wardrobe_prints = StringField()

    # 9. Jewelry in your wardrobe – what and how many of them?
    wardrobe_jewelry = StringField()

    # 10. Makeup – what do you usually do?
    makeup_routine = StringField()

    # 11. Do you have a lot of shoes and do you wear heels?
    shoe_collection = StringField()

    # 12. How often do you change your hairstyles and hair color?
    hairstyle_frequency = StringField()

    # 13. Are you so comfortable or does this outfit depend on the circumstances?
    outfit_comfort = StringField()

    # 14. Are you a fan of noisy parties, holidays, or social events? If you need to go, how will you behave?
    social_event_preference = StringField()

    # 15. What is your dream car?
    dream_car = StringField()

    # 16. How did you study at school? What sports sections did you attend and why?
    school_performance = StringField()

    # 17. What do you do? Is there a dress code? Do you like this job?
    profession = StringField()

    # 18. What impression do you want to make?
    desired_impression = StringField()

    # 19. What is your lifestyle or schedule (business trips, receptions, lots of sports, travel, nightlife)?
    lifestyle_schedule = StringField()

    def to_string(self):
        values = [value for key, value in self._data.items()]
        zipped_list = zip(questions, values)
        return "\n".join([f"{item[0]}\n{item[1]}" for item in zipped_list])
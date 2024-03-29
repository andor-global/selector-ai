from transformers import AutoFeatureExtractor, SegformerForSemanticSegmentation
from PIL import Image
import torch.nn as nn

extractor = AutoFeatureExtractor.from_pretrained("mattmdjaga/segformer_b2_clothes")
model = SegformerForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes")


def segment_items(image):
    inputs = extractor(images=image, return_tensors="pt")

    outputs = model(**inputs)
    logits = outputs.logits.cpu()

    upsampled_logits = nn.functional.interpolate(
        logits,
        size=image.size[::-1],
        mode="bilinear",
        align_corners=False,
    )

    pred_seg = upsampled_logits.argmax(dim=1)[0]

    # Extract the upper cloth mask
    clothes_dict = {17: 'Scarf', 16: 'Bag', 10: 'Right-shoe', 9:'Left-shoe', 8: 'Belt', 7: 'Dress', \
                    6: 'Pants', 5: 'Skirt', 4: 'Upper-clothes', 3: 'Sunglasses', 1: 'Hat'}

    cloth_labels = [17, 16, 10, 9, 8, 7, 6, 5, 4, 3, 1]  # Replace with the actual label index for the upper cloth
    upper_cloth_mask = [seg for seg in pred_seg if seg in cloth_labels]

    # Plot and display the upper cloth mask
    plt.imshow(upper_cloth_mask)
    plt.show()
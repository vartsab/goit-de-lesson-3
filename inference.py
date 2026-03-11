import argparse
from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms


def load_labels():
    """
    Повертає список назв класів.
    Якщо labels.txt існує — читаємо його.
    Якщо ні — створюємо запасний список class_0 ... class_999.
    """
    labels_path = Path("labels.txt")

    if labels_path.exists():
        with open(labels_path, "r", encoding="utf-8") as f:
            labels = [line.strip() for line in f if line.strip()]
        if len(labels) == 1000:
            return labels

    return [f"class_{i}" for i in range(1000)]


def preprocess_image(image_path: str):
    """
    Завантажує зображення та готує його для моделі ImageNet.
    """
    image = Image.open(image_path).convert("RGB")

    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    tensor = transform(image).unsqueeze(0)  # додаємо batch dimension
    return tensor


def predict(model_path: str, image_path: str, top_k: int = 3):
    """
    Завантажує TorchScript модель, запускає inference і повертає top-k результатів.
    """
    model = torch.jit.load(model_path, map_location="cpu")
    model.eval()

    input_tensor = preprocess_image(image_path)
    labels = load_labels()

    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        top_probs, top_indices = torch.topk(probabilities, top_k)

    results = []
    for prob, idx in zip(top_probs, top_indices):
        class_index = idx.item()
        class_name = labels[class_index] if class_index < len(labels) else f"class_{class_index}"
        results.append((class_name, float(prob.item())))

    return results


def main():
    parser = argparse.ArgumentParser(description="TorchScript image inference")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--model", default="model.pt", help="Path to TorchScript model")
    parser.add_argument("--top_k", type=int, default=3, help="Number of top predictions")

    args = parser.parse_args()

    if not Path(args.image).exists():
        raise FileNotFoundError(f"Image file not found: {args.image}")

    if not Path(args.model).exists():
        raise FileNotFoundError(f"Model file not found: {args.model}")

    results = predict(args.model, args.image, args.top_k)

    print("Top predictions:")
    for i, (class_name, probability) in enumerate(results, start=1):
        print(f"{i}. {class_name}: {probability:.4f}")


if __name__ == "__main__":
    main()

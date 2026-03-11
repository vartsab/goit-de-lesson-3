import torch
from torchvision import models


def main():
    # Завантажуємо pretrained модель MobileNetV2
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

    # Переводимо модель у режим inference
    model.eval()

    # Створюємо тестовий вхід для TorchScript
    example_input = torch.randn(1, 3, 224, 224)

    # Конвертуємо модель у TorchScript
    scripted_model = torch.jit.trace(model, example_input)

    # Зберігаємо модель
    scripted_model.save("model.pt")

    print("Model exported successfully → model.pt")


if __name__ == "__main__":
    main()

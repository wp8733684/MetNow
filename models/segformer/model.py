import torch
from torch import Tensor
from torch.nn import functional as F
from models.segformer.parts import *


class SegFormer(BaseModel):
    def __init__(self, num_inchannels: int = 3, num_classes: int = 19, backbone: str = 'MiT-B0') -> None:
        super().__init__(backbone, num_inchannels, num_classes)
        # self.decode_head = SegFormerHead(self.backbone.channels, 256 if 'B0' in backbone or 'B1' in backbone else 768, num_classes)
        self.decode_head = FPNHead(self.backbone.channels, 256 if 'B0' in backbone or 'B1' in backbone else 768, num_classes)
        self.apply(self._init_weights)

    def forward(self, x: Tensor) -> Tensor:
        y = self.backbone(x)
        y = self.decode_head(y)   # 4x reduction in image size
        y = F.interpolate(y, size=x.shape[2:], mode='bilinear', align_corners=False)    # to original image shape
        return y


if __name__ == '__main__':
    model = SegFormer(4, 8, 'MiT-B0')
    # model.load_state_dict(torch.load('checkpoints/pretrained/segformer/segformer.b0.ade.pth', map_location='cpu'))
    x = torch.zeros(1, 4, 512, 512)
    y = model(x)
    print(y.shape)
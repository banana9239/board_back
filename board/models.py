from django.db import models
from common.models import CommonModel

class LargeCategory(CommonModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class MediumCategory(CommonModel):
    name = models.CharField(max_length=50, unique=True)
    large_category = models.ForeignKey(
        'LargeCategory',
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return f'{self.large_category} > {self.name}'

class SmallCategory(CommonModel):
    name = models.CharField(max_length=50)
    medium_category = models.ForeignKey(
        'MediumCategory',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.medium_category} > {self.name}'

class Board(CommonModel):
    board_name = models.CharField(max_length=50)
    board_category = models.ForeignKey(
        'SmallCategory',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.board_name


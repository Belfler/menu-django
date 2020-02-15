from django.db import models
from django.shortcuts import resolve_url
from django.urls.exceptions import NoReverseMatch

__all__ = ['Menu', 'MenuPoint', 'Relation']


class Menu(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title[:10]


class MenuPoint(models.Model):
    menu = models.ForeignKey('Menu', related_name='points', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='children')
    depth = models.PositiveSmallIntegerField(default=0, editable=False)

    class Meta:
        unique_together = ['menu', 'url_name']

    def __str__(self):
        return self.title[:10]

    def save(self, *args, **kwargs):
        if not self.url_name_exists():
            raise NoReverseMatch(f"There is no url with name '{self.url_name}'")
        self.depth = self.parent.depth + 1 if self.parent else 0
        super(MenuPoint, self).save(*args, **kwargs)
        if self.parent:
            self.create_relations()

    def url_name_exists(self):
        try:
            resolve_url(self.url_name)
        except NoReverseMatch:
            return False
        return True

    def create_relations(self):
        relations_of_parent = Relation.objects.filter(descendant=self.parent).values_list('ancestor_id', 'power')
        relations = []
        for ancestor_id, power in relations_of_parent:
            relations.append(Relation(ancestor_id=ancestor_id, descendant=self, power=power + 1))
        relations.append(Relation(ancestor=self.parent, descendant=self, power=1))
        Relation.objects.bulk_create(relations)


class Relation(models.Model):
    """Relation of ancestor with all its descendants."""
    ancestor = models.ForeignKey('MenuPoint', on_delete=models.CASCADE, related_name='relations_with_descendants')
    descendant = models.ForeignKey('MenuPoint', on_delete=models.CASCADE, related_name='relations_with_ancestors')
    # Number of edges between ancestor and descendant.
    power = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"'{self.ancestor}'->'{self.descendant}':{self.power}"

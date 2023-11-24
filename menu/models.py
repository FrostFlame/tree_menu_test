from django.db import models


# Create your models here.


class MenuItem(models.Model):
    title = models.CharField(verbose_name='Название', max_length=30, unique=True)
    url = models.CharField(verbose_name='Ссылка', max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name='Родитель', related_name='children',
                               on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

    def get_tree(self):
        tree_list = MenuItem.objects.raw('''
            WITH RECURSIVE tree(id, title, url, parent_id, path) AS (
                SELECT id, title, url, parent_id, CAST(id AS TEXT) AS path
                FROM menu_menuitem
                WHERE id = %s
                UNION ALL
                SELECT t.id, t.title, t.url, t.parent_id, rec.path || ' ' || t.id
                FROM menu_menuitem AS t, tree AS rec
                WHERE t.parent_id = rec.id
            )
            SELECT id, title, url, path FROM tree
            ORDER BY path
        ''', [self.id])

        tree = {}
        for item in tree_list:
            current_level = tree
            for step in item.path.split(' '):
                if step not in current_level:
                    current_level[step] = {'data': item}
                current_level = current_level[step]
        return tree

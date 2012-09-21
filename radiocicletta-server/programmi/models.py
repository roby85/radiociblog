from django.db import models
from djangotoolbox.fields import ListField
from blog.models import Blog
from random import choice
from string import ascii_letters, digits
import re
from django.core.cache import cache


PROGSTATUS=(
('0','ferie (offair)'),
('1','in programmazione'),
('2','special'),    
('3','cambiato'),
('4','nuovo'),
('5','replica'))
#un sacco di modi piu fichi per farlo ma google di memoria ce ne regala a pacchi
PRIMA={'lu':'do','ma':'lu','me':'ma','gi':'me','ve':'gi','sa':'ve','do':'lu','s':'s'}
GIORNI=(('lu','LUNEDI'),('ma','MARTEDI'),('me','MERCOLEDI'),('gi','GIOVEDI'),('ve','VENERDI'),('sa','SABATO'),('do','DOMENICA'),('s','SINGOLO'))


def default_blog():
    blogs = Blog.objects.all()[:1]
    if blogs:
        return blogs[0]
    return None

class Programmi(models.Model):
    title = models.CharField(max_length=200,help_text='Titolo del programma')
    descr = models.CharField(null=True, blank=True, max_length=200,help_text='descrizione (opzionale)')
    blog = models.ForeignKey(Blog, related_name='programs', default=default_blog, help_text='il blog del programma oppure null')
    status = models.CharField(max_length=1, choices=PROGSTATUS)
    startgiorno = models.CharField(max_length=2, choices=GIORNI, help_text='Scegliere il giorno oppure SINGOLO se si ripete solo una volta')
    startora = models.TimeField(help_text='ora di inizio (nel formato hh:mm:ss con hh da 00 a 23)')
    endgiorno = models.CharField(max_length=2, choices=GIORNI)
    endora = models.TimeField()
    successivo = models.BooleanField(default=False,help_text="Check se l'orario del programma sconfina al giorno successivo (supera le 23.59)")
    #next = models.ForeignKey('Programmi', null=True, blank=True,related_name='seguente', default=None, help_text='il programma successivo (se esiste)')
    
    def __unicode__(self):
        return self.title
    #preparo il json e scalo il giorno se il programma scavalla la mezzanotte (il js che renderizza se n'ha a male altrimenti)


    def get_blog(self):
        cached_blog = cache.get('programma_%s_blog' % self.pk)
        if not cached_blog:
            cache.set('programma_%s_blog' % self.pk, self.blog)
            return self.blog
        return cached_blog

    def tojson(self):
        blog = self.get_blog()
        return {self.title:{ "id":self.id,
                 "start": [self.startgiorno,self.startora.hour,self.startora.minute],
                 "end": [self.endgiorno if not self.successivo else PRIMA[self.endgiorno],self.endora.hour,self.endora.minute],
                 "stato":self.status,
                 "blog_id":blog.id,
                 "blog_url":blog.url,
                 "logo":blog.get_logo().to_json()}
                }

    #def mynext(self):
    #    if self.next:
    #        return (str(self.id),str(self.next.id))
    #    else:
    #        return None

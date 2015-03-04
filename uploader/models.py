from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
import sys, zipfile, os, os.path
from django.template.defaultfilters import slugify
from PIL import Image
import shutil

class Event(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.name
    
class Upload(models.Model):
    event = models.ForeignKey(Event)
    file = models.FileField(null=False, blank=False, upload_to="uploads")
 
    def __unicode__(self):
        return "%s for %s" % (self.file, self.event)
    
    def path(self):
        return "%s" % self.file
    
    def extract(self):
        zip = zipfile.ZipFile(self.file)
        outpath = "public/media/" + self.path().replace(".zip", "")
        os.mkdir(outpath)
        
        for name in zip.namelist():
            zip.extract(name, outpath)
        for file in os.listdir(outpath):
            infile = outpath + "/" + file
            outfile = outpath + "/" + file.replace(' ', '-')    
            os.rename(infile, outfile)
            
            try:
                test_image = Image.open(outfile)
                test_image.verify()
                self.make_picture(outfile)
            except:
                try:
                    os.remove(outfile)
                except:
                    shutil.rmtree(outfile)
                    
            

    def make_picture(self, path):
        pic = Picture()
        pic.event = self.event
        pic.Upload = self
        pic.image = path.replace('public/media/', '')
        pic.save()
        
        
class Picture(models.Model):
    event = models.ForeignKey(Event)
    Upload = models.ForeignKey(Upload)
    image = models.ImageField(upload_to="uploads")
        
    @property
    def file_name(self):
        name = "%s" % self.image
        namelist = name.split('/')
        return "%s" % namelist[2]

        
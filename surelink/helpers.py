import hashlib

class SureLink:
    def __init__(self,filename,width,height,captions,poster,protection,authtype,player,
                 protection_key):
        self.filename = filename
        self.width = width
        self.height = height
        self.captions = captions
        self.poster = poster
        self.protection = protection
        self.authtype = authtype
        self.player = player
        self.protection_key = protection_key

    def test(self):
        if self.player == "test":
            return "new"
        else:
            return ""

    def get_protection(self,force_public=False):
        if force_public:
            protection = "public"
        else:
            protection = self.protection
        s = "%s:%s:%s" % (self.filename,protection,self.protection_key)
        return hashlib.sha1(s).hexdigest()        

    def player_string(self):
        if self.protection == "public-mp4-download":
            return 'download_mp4_v3'
        else:
            if self.player is None:
                return 'v3'
        return self.player

    def captions_string(self):
        if self.captions:
            return "&captions=%s" % self.captions
        return ""

    def authtype_string(self):
        if self.authtype:
            return "&authtype=%s" % self.authtype
        return ""

    def video_options(self):
        if self.poster == 'default_custom_poster':
            if 'secure' not in self.filename:
                # secure: parallel dir as video file in /broadcast/posters/
                poster = "http://ccnmtl.columbia.edu/broadcast/posters/" + self.filename.replace('.mp4','.jpg').replace('.flv','.jpg')
            else:
                # insecure: same dir as video file
                poster = "http://ccnmtl.columbia.edu/broadcast/" + self.filename.replace('.mp4','.jpg').replace('.flv','.jpg')

        return "player=%s&file=%s&width=%d&height=%d&poster=%s%s%s" % \
            (self.player_string(),self.filename,self.width,self.height,self.poster,self.captions_string(),
             self.authtype_string())

    def src_url(self):
        return "http://ccnmtl.columbia.edu/stream/%sjsembed?%s%s" % (self.test(),self.video_options(),
                                                                     self.protection_string())

    def public_url(self):
        return "http://ccnmtl.columbia.edu/stream/flv/%s/OPTIONS/%s" % (self.get_protection(force_public=True),self.filename)

    def group(self):
        if self.protection.startswith('public'):
            return 'public'
        else:
            return self.protection

    def protection_string(self):
        if self.protection.startswith('public'):
            return "&protection=%s" % self.get_protection(force_public=True)
        return ""

    def public_mp4_download(self):
        return self.protection == "public-mp4-download"

    

    ##### Nitty-gritty embed codes! #####

    def basic_embed(self):
         return """<script type="text/javascript" src="%s"></script>""" % self.src_url()
    
    def iframe_embed(self):
        return """<iframe width="%d" height="%d" src="https://surelink.ccnmtl.columbia.edu/video/?%s%s" />""" \
            % (self.width,self.height+24,self.video_options(),self.protection_string())

    def edblogs_embed(self):
        return """[ccnmtl_video src="%s"]""" % self.src_url()

    def drupal_embed(self):
        return "http://ccnmtl.columbia.edu/stream/flv/xdrupalx/OPTIONS/%s" % self.filename

    def mdp_embed(self):
        width_string = ""
        if self.width: 
            width_string = "[w]%d" % self.width
        height_string = ""
        if self.height: 
            height_string = "[h]%d" % self.height

        if self.public_mp4_download():
            return """[mp4]http://ccnmtl.columbia.edu/broadcast/%s%s%s[mp4]""" % (self.filename,width_string,height_string)
        else:
            return """[flv]%s%s%s[flv]""" % (self.public_url(),width_string,height_string)


def protection(filename,group,protection_key):
    s = "%s:%s:%s" % (filename,group,protection_key)
    return hashlib.sha1(s).hexdigest()        

def protection_string(filename,group,protection_key):
    if group.startswith('public'):
        return "&protection=%s" % protection(filename,'public',protection_key)
    return ""

def video_options(protection,file,width,height,poster,player=None,
                  captions=None,authtype=None):
    if protection == "public-mp4-download":
        player = 'download_mp4_v3'
    else:
        if player is None:
            player = 'v3'

    if poster == 'default_custom_poster':
        if 'secure' not in file:
            # secure: parallel dir as video file in /broadcast/posters/
            poster = "http://ccnmtl.columbia.edu/broadcast/posters/" + file.replace('.mp4','.jpg').replace('.flv','.jpg')
        else:
            # insecure: same dir as video file
            poster = "http://ccnmtl.columbia.edu/broadcast/" + file.replace('.mp4','.jpg').replace('.flv','.jpg')
    captions_string = ""
    if captions:
        captions_string = "&captions=%s" % captions

    authtype_string = ""
    if authtype:
        authtype_string = "&authtype=%s" % authtype
    return "player=%s&file=%s&width=%d&height=%d&poster=%s%s%s" % \
        (player,file,width,height,poster,captions_string,authtype_string)

def src_url(test,vid_options,filename,protection,protection_key):
    return "http://ccnmtl.columbia.edu/stream/%sjsembed?%s%s" % (test,vid_options,protection_string(filename,protection,protection_key))



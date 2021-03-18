from django import template

register = template.Library()

COLORS = ["","#FFFFFF","#FFFFCC","#FFFF99","#FFFF88","#FFFF77","#FFFF66","#FFFF55","#FFFF44","#FFFF33","#FFFF22",
          "#FFFF11","#FFFF00","#FFCC00","#FF9900","#FF8800","#FF7700","#FF6600","#FF5500","#FF4400","#FF3300",
          "#FF2200","#FF1100","#FF0000","#CC0000","#990000","#880000","#770000","#660000","#550000","#440000"
          ]


@register.filter(name='caracolor')
def caracolor(value):
    if value == None or value == '-':
        return ' '
    else :
        return COLORS[int(value)]
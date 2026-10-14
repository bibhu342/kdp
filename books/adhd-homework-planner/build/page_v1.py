from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black
W,H=letter; M=0.6*72; c=canvas.Canvas("sample_v1.pdf",pagesize=letter)
G=HexColor("#555555"); L=HexColor("#BBBBBB")
def box(x,y,w,h,title):
    c.setStrokeColor(black); c.setLineWidth(1.4); c.roundRect(x,y,w,h,8)
    c.setFont("Helvetica-Bold",11); c.drawString(x+8,y+h-16,title)
def lines(x,y,w,top,n,gap):
    c.setStrokeColor(L); c.setLineWidth(0.6)
    for i in range(n): c.line(x+8,top-i*gap,x+w-8,top-i*gap)
y=H-M
c.setFont("Helvetica-Bold",22); c.drawString(M,y-20,"TODAY'S PLAN")
c.setFont("Helvetica",10); c.setFillColor(G)
c.drawRightString(W-M,y-8,"Date: ____ / ____ / ______"); 
days="M  T  W  Th  F  Sa  Su"; c.drawRightString(W-M,y-24,"Circle:  "+days); c.setFillColor(black)
y-=40; cw=W-2*M
# Top 3
h=78; box(M,y-h,cw,h,"MY TOP 3 (just these!)")
for i in range(3):
    yy=y-36-i*16; c.rect(M+12,yy-2,10,10); c.setStrokeColor(L); c.line(M+30,yy-2,M+cw-12,yy-2); c.setStrokeColor(black)
y-=h+10
# homework table
h=210; box(M,y-h,cw,h,"HOMEWORK")
cols=[("Subject",0.22),("What to do",0.50),("Due",0.14),("Done",0.14)]
c.setFont("Helvetica-Bold",9); xx=M+8; tw=cw-16; hy=y-34
for name,f in cols: c.drawString(xx+3,hy,name); xx+=tw*f
c.setStrokeColor(L); c.setLineWidth(0.6)
for i in range(7):
    ly=hy-6-i*24; c.line(M+8,ly,M+cw-8,ly)
    bx=M+8+tw*0.86+tw*0.07-5; 
    if i<6: c.setStrokeColor(black); c.rect(bx,ly-17,10,10); c.setStrokeColor(L)
xx=M+8
for name,f in cols[:-1]:
    xx+=tw*f; c.line(xx,hy+12,xx,hy-6-6*24)
y-=h+10
# two columns
hw=(cw-10)/2; h=150
box(M,y-h,hw,h,"BRAIN DUMP"); c.setFont("Helvetica-Oblique",8); c.setFillColor(G); c.drawString(M+8,y-28,"Empty your head here, sort it later."); c.setFillColor(black)
x2=M+hw+10; box(x2,y-h,hw,h,"PACK MY BAG")
items=["Homework folder","Books / laptop","Charger","Water bottle","Lunch / snack","Signed forms","",""]
c.setFont("Helvetica",10)
for i,t in enumerate(items):
    yy=y-34-i*14.5; c.rect(x2+12,yy-1,9,9); 
    if t: c.drawString(x2+28,yy,t)
    else: c.setStrokeColor(L); c.line(x2+28,yy-1,x2+hw-12,yy-1); c.setStrokeColor(black)
y-=h+10
# focus timer + energy
h=72; box(M,y-h,hw,h,"FOCUS SPRINTS (colour one per 20 min)")
for i in range(8): c.circle(M+24+i*(hw-40)/7,y-48,10)
box(x2,y-h,hw,h,"HOW I FELT TODAY")
c.setFont("Helvetica",9)
for i,t in enumerate(["Focus","Energy","Mood"]):
    yy=y-32-i*14; c.drawString(x2+10,yy,t)
    for j in range(5): c.circle(x2+70+j*20,yy+3,5)
y-=h+10
h=y-M; box(M,M,cw,h,"WIN OF THE DAY")
lines(M,M,cw,M+h-34,1,0)
c.setFont("Helvetica",7); c.setFillColor(G); c.drawCentredString(W/2,M-14,"Done is better than perfect.")
c.save()
import fitz; d=fitz.open("sample_v1.pdf"); d[0].get_pixmap(dpi=110).save("sample_v1.png")

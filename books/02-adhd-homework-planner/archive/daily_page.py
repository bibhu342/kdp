from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
W,H=letter; M=0.55*72; c=canvas.Canvas("sample_v2_APPROVED.pdf",pagesize=letter)
GR=HexColor("#D9D9D9"); LT=HexColor("#F0F0F0"); L=HexColor("#AAAAAA"); G=HexColor("#555555")
cw=W-2*M
def box(x,y,w,h,title,sub=None):
    c.setStrokeColor(black); c.setLineWidth(1.2); c.setFillColor(white); c.roundRect(x,y,w,h,7,fill=1)
    c.setFillColor(GR); c.roundRect(x,y+h-20,w,20,7,fill=1,stroke=0); c.rect(x,y+h-20,w,8,fill=1,stroke=0)
    c.setStrokeColor(black); c.roundRect(x,y,w,h,7)
    c.setFillColor(black); c.setFont("Helvetica-Bold",10.5); c.drawString(x+8,y+h-14,title)
    if sub: c.setFont("Helvetica-Oblique",7.5); c.setFillColor(G); c.drawRightString(x+w-8,y+h-14,sub); c.setFillColor(black)
def ln(x1,y,x2): c.setStrokeColor(L); c.setLineWidth(0.6); c.line(x1,y,x2,y); c.setStrokeColor(black)
def cb(x,y,s=9): c.setLineWidth(0.9); c.rect(x,y,s,s)
def dot(x,y,r=6): c.setFillColor(LT); c.setLineWidth(0.9); c.circle(x,y,r,fill=1); c.setFillColor(black)
y=H-M
c.setFont("Helvetica-Bold",21); c.drawString(M,y-18,"TODAY'S PLAN")
c.setFont("Helvetica",9.5); c.setFillColor(G); c.drawRightString(W-M,y-7,"Date: ____ / ____ / ______")
c.drawRightString(W-M,y-21,"Circle:  M   T   W   Th   F   Sa   Su"); c.setFillColor(black)
y-=32
# Recharge first
h=36; box(M,y-h,cw,h,"RECHARGE FIRST","after school, before homework")
c.setFont("Helvetica",9.5)
for i,t in enumerate(["Snack","Water","Move 10 min","Quiet time"]):
    x=M+12+i*(cw-24)/4; cb(x,y-31); c.drawString(x+14,y-30,t)
y-=h+7
# Top 3 + first step
h=82; box(M,y-h,cw,h,"MY TOP 3","+ the tiny 2-minute first step")
c.setFont("Helvetica-Bold",8); c.setFillColor(G); c.drawString(M+30,y-31,"Task"); c.drawString(M+cw*0.55,y-31,"Tiny first step"); c.setFillColor(black)
for i in range(3):
    yy=y-47-i*15; cb(M+12,yy); ln(M+30,yy,M+cw*0.52); ln(M+cw*0.55,yy,M+cw-12)
y-=h+7
# Homework with time guess
h=176; box(M,y-h,cw,h,"HOMEWORK","guess the time, then check it")
tw=cw-16; cols=[("Subject",0.17),("Steps (write them all down)",0.47),("Guess",0.11),("Real",0.11),("Done",0.14)]
c.setFont("Helvetica-Bold",8.5); xx=M+8; hy=y-33
for n,f in cols: c.drawString(xx+3,hy,n); xx+=tw*f
rows=6; rh=21
for i in range(rows+1): ln(M+8,hy-5-i*rh,M+cw-8)
xx=M+8
for n,f in cols[:-1]:
    xx+=tw*f; c.setStrokeColor(L); c.line(xx,hy+11,xx,hy-5-rows*rh); c.setStrokeColor(black)
c.setFont("Helvetica",7.5); c.setFillColor(G)
for i in range(rows):
    yb=hy-5-(i+1)*rh+6
    c.drawRightString(M+8+tw*0.75-4,yb,"min"); c.drawRightString(M+8+tw*0.86-4,yb,"min")
    c.setFillColor(black); cb(M+8+tw*0.93-4,yb-1); c.setFillColor(G)
c.setFillColor(black)
y-=h+7
# Focus sprints + parking lot
hw=(cw-8)/2; h=104; x2=M+hw+8
box(M,y-h,hw,h,"FOCUS SPRINTS","fill one per 20 min")
for r in range(2):
    for i in range(4):
        cx=M+28+i*((hw-40)/3.3); cy=y-42-r*32; dot(cx,cy,10)
        if i<3: c.setFont("Helvetica",6.5); c.setFillColor(G); c.drawCentredString(cx+(hw-40)/6.6,cy-3,"move!"); c.setFillColor(black)
c.setFont("Helvetica",7.5); c.drawString(M+10,y-h+7,"Hyperfocus alarm: stop at ____:____")
box(x2,y-h,hw,h,"DISTRACTION PARKING LOT","park it, do it later")
for i in range(4): ln(x2+10,y-38-i*17,x2+hw-10)
y-=h+7
# Before I hand it in + feelings
h=100
box(M,y-h,hw,h,"BEFORE I HAND IT IN")
c.setFont("Helvetica",9)
for i,t in enumerate(["Name + date on it","Every question answered","Read the instructions again","Checked one more time","In my folder / sent"]):
    yy=y-36-i*13.5; cb(M+12,yy); c.drawString(M+26,yy+1,t)
box(x2,y-h,hw,h,"HOW I FELT TODAY")
c.setFont("Helvetica",8.5)
for i,t in enumerate(["Focus","Energy","Mood"]):
    yy=y-36-i*13; c.drawString(x2+10,yy,t)
    for j in range(5): dot(x2+68+j*18,yy+3,5)
c.setFont("Helvetica-Bold",8); c.drawString(x2+10,y-h+22,"If a friend had my day, I'd tell them:")
ln(x2+10,y-h+9,x2+hw-10)
y-=h+7
# Win + reward
h=y-M; box(M,M,cw,h,"WIN OF THE DAY","+ my reward")
c.setFont("Helvetica",9); c.drawString(M+12,M+h-36,"Today I did:"); ln(M+75,M+h-37,M+cw-12)
c.drawString(M+12,M+h-54,"My reward:"); ln(M+75,M+h-55,M+cw-12)
c.setFont("Helvetica-Oblique",7); c.setFillColor(G); c.drawCentredString(W/2,M-13,"Mistakes help my brain grow. Done is better than perfect.")
c.save()

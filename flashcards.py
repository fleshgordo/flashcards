#!/usr/bin/python

# Creates flashcards or any other card deck with front and backside for double-side print
# Needs a CSV file for content
# Open in scribus as executable script
# Adapt to your needs and print 

# Tested with Scribus 1.5
# Written by Gordan Savicic (March 2022)

DEBUG = False # True to try script without scribus
page_width = 210 # page dimension in mm 
page_height = 297
margin_y = 10 # vertical margin 

# total amount of cards in deck
cards = 71
cards_per_page = 10 # needs to multiple of 2
cards_per_row = 2 # set how many cards per row
card_width = 80 # width in mm
card_height = 50 # height in mm

font_size = 20
csv_filename = "cards.csv" # csv file, should be formatted: frontside, backside\r\n

# nothing needs to be changed below this part

if DEBUG == False:
    from scribus import *
    newDoc((page_width, page_height), (10, 10, 10, 10), PORTRAIT, 1, UNIT_MILLIMETERS, FACINGPAGES, FIRSTPAGELEFT)


words_per_page = cards_per_page / 2
card_rows = cards_per_page / cards_per_row

pages = cards/words_per_page
print("Total pages: %d" %pages)
print("Card rows: %d"%card_rows)

for i in range(pages) :
    if DEBUG == False:
        newPage(-1)
    print("create new page %s"%i)

with open (csv_filename) as f:
    current_page = 1
    index = 0
    if DEBUG == False:
        gotoPage(current_page)

    # calculate x positions for cards (from page center)
    card_pos_x_1 = page_width * .5 - card_width
    card_pos_x_2 = page_width * .5 

    for i,words in enumerate(f.readlines()):        
        text_topic = words.strip().split(",")[0] # get card frontside
        text_value = words.strip().split(",")[1] # get card backside
        if index == 0:
            old_topic = text_topic
        #print(index)
     
        # force page break and fill up with remaining topic names (important for double-side print
        # todo: fill with addtional page in case page numbers for category is not even! 
        if (text_topic != old_topic):
            while (index % card_rows != 0) :
                if DEBUG == False:
                    card_pos_y_1 = (page_height - (card_rows * card_height) - 2 * margin_y) * .5 + card_height * ((index % card_rows)) + margin_y
                    createRect(card_pos_x_1,card_pos_y_1,card_width,card_height)
                    left_box = createText(card_pos_x_1,card_pos_y_1,card_width,card_height,text_topic)
                    setText(old_topic,left_box)
                    setTextAlignment(ALIGN_CENTERED, left_box)
                    setTextVerticalAlignment(ALIGN_CENTERED, left_box)
                    setFontSize(font_size, left_box)
                    index+=1
      
            index = 0
            current_page+=1
            print("!!!!--- " )
            print("goto page %s"%current_page)    
            if DEBUG == False:
                gotoPage(current_page)     

        # calculate y position for card + text
        card_pos_y_1 = (page_height - (card_rows * card_height) - 2 * margin_y) * .5 + card_height * ((index % card_rows)) + margin_y
 
  
        if DEBUG == True:
            print("createRect(%d, %d, %d, %d)" %(card_pos_x_1,card_pos_y_1,card_width,card_height))
            print("createText(%d, %d, %d, %d, %s)" %(card_pos_x_1,card_pos_y_1,card_width,card_height,text_topic))
            print("createText(%d, %d, %d, %d, %s)" %(card_pos_x_2,card_pos_y_1,card_width,card_height,text_value))
        
        # scribus, create rects and textboxes + align them
        if DEBUG == False:
            createRect(card_pos_x_1,card_pos_y_1,card_width,card_height)
            createRect(card_pos_x_2,card_pos_y_1,card_width,card_height)
            left_box = createText(card_pos_x_1,card_pos_y_1,card_width,card_height,text_topic)
            right_box = createText(card_pos_x_2,card_pos_y_1,card_width,card_height,text_value)
            setText(text_topic,left_box)
            setText(text_value,right_box) 
            setTextAlignment(ALIGN_CENTERED, left_box)
            setTextVerticalAlignment(ALIGN_CENTERED, left_box)
            setTextAlignment(ALIGN_CENTERED, right_box)
            setTextVerticalAlignment(ALIGN_CENTERED, right_box)
            setFontSize(font_size, left_box)
            setFontSize(font_size, right_box)   

        old_topic = text_topic # needed for category change detection
        index+=1
        
        # if reaching card per page limit create new Page
        if (index % card_rows == 0) :
            index = 0
            current_page+=1
            print("-------------------------")
            print("goto page %s"%current_page)
            if DEBUG == False:
                gotoPage(current_page)

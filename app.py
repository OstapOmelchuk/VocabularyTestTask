from tkinter import *
from tkinter import ttk

from db.db_managment import (
    save_new_word, delete_word, add_new_vocabulary, replace_vocabulary, get_suitable_for_condition_words
)


def only_letters(char):
    return char.isalpha()


root = Tk()
root.title("Vocabulary")
root.geometry("700x600")

validation = root.register(only_letters)

tabControl = ttk.Notebook(root)

main_tab = ttk.Frame(tabControl)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(main_tab, text='Main')
tabControl.add(tab1, text='Add/Delete word')
tabControl.add(tab2, text='Add/Replace vocabulary')
tabControl.add(tab3, text='Find suitable for condition words')
tabControl.pack(expand=1, fill="both")


# # # # # # # _Main_Tab_ # # # # # # #


main_canvas = Canvas(main_tab, height=600, width=700, bg='#5c8dcc')
main_canvas.place(x=0, y=0)

select_option_label = Label(
    main_canvas, text="Choose an option:", justify=CENTER, font=('Helvatical bold', 30), bg="#3267ab"
)
select_option_label.place(x=170, y=70)

ad_word_button = Button(
    main_canvas, text="Add/Delete word", command=lambda: tabControl.select(tab1), width=15, height=5, bg="#3267ab"
)
ad_word_button.place(x=270, y=180)

loan_vocabulary_button = Button(
    main_canvas,
    text="Add/Replace vocabulary",
    command=lambda: tabControl.select(tab2),
    width=20,
    height=5,
    bg="#3267ab"
)
loan_vocabulary_button.place(x=250, y=300)

loan_vocabulary_button = Button(
    main_canvas,
    text="Find suitable for condition words",
    command=lambda: tabControl.select(tab3),
    width=25,
    height=5,
    bg="#3267ab"
)
loan_vocabulary_button.place(x=230, y=420)


# # # # # # # _Tab1_ # # # # # # #


tab1_canvas = Canvas(tab1, height=600, width=700, bg='#5c8dcc')
tab1_canvas.place(x=0, y=0)

add_word_label = Label(tab1_canvas, text="Add a word to your vocabulary:", font=('Helvatical bold', 20), bg="#3267ab")
add_word_label.place(x=20, y=10)

success_add_label = Label(tab1_canvas, text="", font=('Helvatical bold', 10), bg="#3267ab")
success_add_label.place(x=150, y=140)

add_new_word = Entry(tab1_canvas, validate="key", validatecommand=(validation, '%S'), font=('Helvatical bold', 15))
add_new_word.place(x=20, y=60, width=650, height=50)

add_word_btn = Button(
    tab1_canvas,
    text="Add",
    command=lambda: save_new_word(add_new_word.get(), label=success_add_label),
    width=7,
    height=2,
    bg="#3267ab"
)
add_word_btn.place(x=20, y=130)


delete_word_label = Label(
    tab1_canvas, text="Delete a word from your vocabulary:", font=('Helvatical bold', 20), bg="#3267ab"
)
delete_word_label.place(x=20, y=230)

success_delete_label = Label(tab1_canvas, text="", font=('Helvatical bold', 10), bg="#3267ab")
success_delete_label.place(x=150, y=370)

word_to_delete = Entry(tab1_canvas, validate="key", validatecommand=(validation, '%S'), font=('Helvatical bold', 15))
word_to_delete.place(x=20, y=290, width=650, height=50)

delete_word_btn = Button(
    tab1_canvas,
    text="DELETE",
    command=lambda: delete_word(word_to_delete.get(), label=success_delete_label),
    width=7,
    height=2,
    bg="#3267ab"
)
delete_word_btn.place(x=20, y=360)


# # # # # # # _Tab2_ # # # # # # #


tab2_canvas = Canvas(tab2, height=600, width=700, bg='#5c8dcc')
tab2_canvas.place(x=0, y=0)

loan_voc_label = Label(
    tab2_canvas, text="Loan a vocabulary (add/replace)", font=('Helvatical bold', 15), justify=LEFT, bg="#3267ab"
)
loan_voc_label.place(x=10, y=10)

entry_type_label = Label(
    tab2_canvas,
    text="Write words through a comma and a space (aaa, bbb, ..., zzz)",
    font=('Helvatical bold', 15),
    bg="#3267ab"
)
entry_type_label.place(x=15, y=50)

new_voc_text = Text(tab2_canvas, width=82, height=19)
new_voc_text.place(x=15, y=85)

success_label_tab2 = Label(tab2_canvas, text="", bg="#3267ab")
success_label_tab2.place(x=350, y=450)

add_voc_btn = Button(
    tab2_canvas,
    text="Add vocabulary", command=lambda: add_new_vocabulary(
        new_voc_text.get("1.0", END),
        label=success_label_tab2
    ),
    width=15,
    height=3,
    bg="#3267ab"
)
add_voc_btn.place(x=15, y=430)

replace_voc_btn = Button(
    tab2_canvas,
    text="Replace vocabulary", command=lambda: replace_vocabulary(
        new_voc_text.get("1.0", END),
        label=success_label_tab2
    ),
    width=15,
    height=3,
    bg="#3267ab"
)
replace_voc_btn.place(x=180, y=430)


# # # # # # # _Tab3_ # # # # # # #


tab3_canvas = Canvas(tab3, height=600, width=700, bg='#5c8dcc')
tab3_canvas.place(x=0, y=0)

condition_label = Label(
    tab3_canvas,
    text="Enter a condition (letters to find in words)."
         "\nFor example oee -> the word must have one 'o' letter and two letters 'e'",
    justify=LEFT,
    font=('Helvatical bold', 13),
    bg="#3267ab"
)
condition_label.place(x=10, y=1)

entry_condition = Entry(tab3_canvas, validate="key", validatecommand=(validation, '%S'), font=('Helvatical bold', 15))
entry_condition.place(x=10, y=55, width=250, height=30)

suitable_words_label = Label(tab3_canvas, text="", justify=LEFT, bg="#3267ab")
suitable_words_label.place(x=200, y=185)

suitable_words_text = Text(tab3_canvas, width=83, height=17)
suitable_words_text.place(x=10, y=250)

var = IntVar()
var.set(0)

first_10_rdb = Radiobutton(tab3_canvas, text="First 10 words", variable=var, value=0, bg="#3267ab")
first_10_rdb.place(x=10, y=160)
first_50_rdb = Radiobutton(tab3_canvas, text="First 50 words", variable=var, value=1, bg="#3267ab")
first_50_rdb.place(x=10, y=185)
all_suitable_words_rdb = Radiobutton(tab3_canvas, text="All words", variable=var, value=2, bg="#3267ab")
all_suitable_words_rdb.place(x=10, y=210)

add_voc_btn = Button(
    tab3_canvas,
    text="Search",
    command=lambda: get_suitable_for_condition_words(
        entry_condition.get(),
        check=var.get(),
        label=suitable_words_label,
        text=suitable_words_text,
    ),
    width=10,
    height=2,
    bg="#3267ab"
)
add_voc_btn.place(x=10, y=100)

root.mainloop()

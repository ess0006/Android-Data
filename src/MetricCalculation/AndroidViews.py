ANDROID_VIEWS = ["AbsListView",
                "AbsListView.LayoutParams",
                "AbsoluteLayout",
                "AbsoluteLayout.LayoutParams",
                "AbsSeekBar",
                "AbsSpinner",
                "AnalogClock",
                "Button",
                "CalendarView",
                "CheckBox",
                "CheckedTextView",
                "Chronometer",
                "CompoundButton",
                "DatePicker",
                "DigitalClock",
                "EditText",
                "ExpandableListView",
                "ExpandableListView.ExpandableListContextMenuInfo",
                "FrameLayout",
                "FrameLayout.LayoutParams",
                "Gallery",
                "Gallery.LayoutParams",
                "GridLayout",
                "GridLayout.Alignment",
                "GridLayout.LayoutParams",
                "GridLayout.Spec",
                "GridView",
                "HeaderViewListAdapter",
                "HorizontalScrollView",
                "ImageButton",
                "ImageSwitcher",
                "ImageView",
                "LinearLayout",
                "LinearLayout.LayoutParams",
                "ListPopupWindow",
                "ListView",
                "ListView.FixedViewInfo",
                "MediaController",
                "MultiAutoCompleteTextView",
                "MultiAutoCompleteTextView.CommaTokenizer",
                "NumberPicker",
                "OverScroller",
                "PopupMenu",
                "PopupWindow",
                "ProgressBar",
                "QuickContactBadge",
                "RadioButton",
                "RadioGroup",
                "RadioGroup.LayoutParams",
                "RatingBar",
                "RelativeLayout",
                "RelativeLayout.LayoutParams",
                "Scroller",
                "ScrollView",
                "SearchView",
                "SeekBar",
                "SlidingDrawer",
                "Space",
                "Spinner",
                "StackView",
                "Switch",
                "TabHost",
                "TabHost.TabSpec",
                "TableLayout",
                "TableLayout.LayoutParams",
                "TableRow",
                "TableRow.LayoutParams",
                "TabWidget",
                "TextClock",
                "TextView",
                "TimePicker",
                "ToggleButton",
                "VideoView",
                "ZoomButton",
                "ZoomButtonsController",
                "ZoomControls"]

""" Gets a regular expression of all view objects in Android """
def getAndroidViewsRegex():
    regex = "("
    first = True
    for view in ANDROID_VIEWS:
        if not first:
            regex = regex + "|"
        else:
            first = False
        regex = regex + view
    regex = regex + ")"
    return regex
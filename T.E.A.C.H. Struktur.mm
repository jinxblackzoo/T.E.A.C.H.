<map version="freeplane 1.12.1">
<!--To view this file, download free mind mapping software Freeplane from https://www.freeplane.org -->
<node TEXT="T.E.A.C.H. Struktur" LOCALIZED_STYLE_REF="AutomaticLayout.level.root" FOLDED="false" ID="ID_1000000001" CREATED="1748352000000" MODIFIED="1748352108526"><hook NAME="MapStyle">
    <properties fit_to_viewport="false" show_tags="UNDER_NODES" edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" show_icons="BESIDE_NODES"/>
    <tags category_separator="::"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ID="ID_271890427" ICON_SIZE="12 pt" COLOR="#000000" STYLE="fork">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="200" DASH="" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_271890427" STARTARROW="NONE" ENDARROW="DEFAULT"/>
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
<richcontent TYPE="DETAILS" CONTENT-TYPE="plain/auto"/>
<richcontent TYPE="NOTE" CONTENT-TYPE="plain/auto"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.tags">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.selection" BACKGROUND_COLOR="#afd3f7" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#afd3f7"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important" ID="ID_67550811">
<icon BUILTIN="yes"/>
<arrowlink COLOR="#003399" TRANSPARENCY="255" DESTINATION="ID_67550811"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.flower" COLOR="#ffffff" BACKGROUND_COLOR="#255aba" STYLE="oval" TEXT_ALIGN="CENTER" BORDER_WIDTH_LIKE_EDGE="false" BORDER_WIDTH="22 pt" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#f9d71c" BORDER_DASH_LIKE_EDGE="false" BORDER_DASH="CLOSE_DOTS" MAX_WIDTH="6 cm" MIN_WIDTH="3 cm"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10 pt" SHAPE_VERTICAL_MARGIN="10 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<node TEXT="Projektverzeichnis" ID="ID_1000000002" CREATED="1748354703348" MODIFIED="1748354703348">
<node TEXT="src/" ID="ID_1000000003" CREATED="1748352094645" MODIFIED="1748352094645">
<node TEXT="main.py (Startpunkt des Programms, importiert und startet die Hauptanwendung)" ID="ID_MAINPY" CREATED="1748354703348" MODIFIED="1748354703348"/>
<node TEXT="__init__.py (Markiert das Verzeichnis als Python-Paket, technisch erforderlich)" ID="ID_SRC_INITPY" CREATED="1748354703348" MODIFIED="1748354703348"/>
<node TEXT="core/" ID="ID_1000000004" CREATED="1748352094645" MODIFIED="1748352094645">
<node TEXT="__init__.py (Markiert das Verzeichnis als Python-Paket, technisch erforderlich)" ID="ID_CORE_INITPY" CREATED="1748354703348" MODIFIED="1748354703348"/>
<node TEXT="app.py (Hauptanwendung)" ID="ID_1000000006" CREATED="1748352094645" MODIFIED="1748352094645"/>
<node TEXT="module.py (Basisklasse für Module)" ID="ID_1000000007" CREATED="1748352094645" MODIFIED="1748352094645"/>
</node>
<node TEXT="modules/" ID="ID_1000000008" CREATED="1748352094645" MODIFIED="1748352094645">
<node TEXT="VOLL/" ID="ID_1000000009" CREATED="1748352094645" MODIFIED="1748352094645">
<node TEXT="VOLLModuleView.py" ID="ID_1000000010" CREATED="1748352094645" MODIFIED="1748352094645"/>
</node>
<node TEXT="MUT/" ID="ID_1000000011" CREATED="1748352094645" MODIFIED="1748352094645">
<node TEXT="MUTModuleView.py" ID="ID_1000000012" CREATED="1748352094645" MODIFIED="1748352094645"/>
</node>
<node TEXT="KLAR/" ID="ID_1000000013" CREATED="1748352094645" MODIFIED="1748352094645">
<node TEXT="KLARModuleView.py" ID="ID_1000000014" CREATED="1748352094645" MODIFIED="1748352094645"/>
</node>
</node>
</node>
<node TEXT="README.md (Dokumentation)" ID="ID_1000000015" CREATED="1748352094645" MODIFIED="1748352094645"/>
<node TEXT="requirements.txt (Abhängigkeiten)" ID="ID_1000000016" CREATED="1748352094645" MODIFIED="1748352094645"/>
</node>
<node TEXT="Klassendiagramm" ID="ID_1000000017" CREATED="1748352094645" MODIFIED="1748352112902" HGAP_QUANTITY="28.25 pt" VSHIFT_QUANTITY="57.75 pt">
<node TEXT="TEACH (App)" ID="ID_1000000018" CREATED="1748352094645" MODIFIED="1748352094645"/>
<node TEXT="Beschreibung: Hauptklasse der Anwendung. Initialisiert GUI, lädt Module, steuert Programmfluss." ID="ID_1267354561" CREATED="1748354703349" MODIFIED="1748354703349"/>
</node>
</node>
</map>

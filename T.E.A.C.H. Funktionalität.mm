<map version="freeplane 1.12.1">
<!--To view this file, download free mind mapping software Freeplane from https://www.freeplane.org -->
<node TEXT="T.E.A.C.H. Funktionalität" LOCALIZED_STYLE_REF="AutomaticLayout.level.root" FOLDED="false" ID="ID_2000000001" CREATED="1748352100000" MODIFIED="1748352126649">
<node TEXT="Hauptfunktionen" ID="ID_2000000002">
  <node TEXT="Modulverwaltung">
  <node TEXT="ModuleManager (Klasse zur Verwaltung aller Module)"/>
    <node TEXT="Module laden/entladen"/>
    <node TEXT="Module konfigurieren"/>
  </node>
  <node TEXT="KI-Integration">
  <node TEXT="AIService (Klasse für KI-Logik und Regeln)"/>
    <node TEXT="AIService (KI-Funktionen, Regelmanagement)"/>
    <node TEXT="Antwortgenerierung"/>
    <node TEXT="Regelsystem"/>
  </node>
  <node TEXT="Berichtswesen">
  <node TEXT="ReportManager (Klasse für Berichte, PDF-Export, Status)"/>
    <node TEXT="ReportManager (Berichte, PDF-Export, Status)"/>
    <node TEXT="PDF-Export"/>
    <node TEXT="Statusanzeige"/>
  </node>
  <node TEXT="Datenhaltung">
  <node TEXT="DatabaseManager (Klasse für SQLite-Zugriff und Backups)"/>
    <node TEXT="DatabaseManager (Zugriff auf SQLite je Modul)"/>
    <node TEXT="Backup/Restore"/>
  </node>
</node><hook NAME="MapStyle">
    <properties fit_to_viewport="false" edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" show_icons="BESIDE_NODES" show_tags="UNDER_NODES"/>
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
<node TEXT="Hauptfunktionen" ID="ID_2000000002" CREATED="1748352093573" MODIFIED="1748352126649" HGAP_QUANTITY="0.5 pt" VSHIFT_QUANTITY="-54 pt">
<node TEXT="Modulverwaltung" ID="ID_MODULVERWALTUNG">
  <node TEXT="Module laden/entladen"/>
  <node TEXT="Module konfigurieren"/>
</node>
<node TEXT="KI-Integration" ID="ID_KI">
  <node TEXT="AIService (KI-Funktionen, Regelmanagement)"/>
  <node TEXT="Antwortgenerierung"/>
  <node TEXT="Regelsystem"/>
</node>
<node TEXT="Berichtswesen" ID="ID_BERICHT">
  <node TEXT="ReportManager (Berichte, PDF-Export, Status)"/>
  <node TEXT="PDF-Export"/>
  <node TEXT="Statusanzeige"/>
</node>
<node TEXT="Datenhaltung" ID="ID_DH">
  <node TEXT="DatabaseManager (Zugriff auf SQLite je Modul)"/>
  <node TEXT="Backup/Restore"/>
</node>
<node TEXT="Modulverwaltung" ID="ID_2000000003" CREATED="1748352093573" MODIFIED="1748352093573">
<node TEXT="Module laden/entladen" ID="ID_2000000004" CREATED="1748352093573" MODIFIED="1748352093573"/>
<node TEXT="Module konfigurieren" ID="ID_2000000005" CREATED="1748352093574" MODIFIED="1748352093574"/>
</node>
<node TEXT="KI-Integration" ID="ID_2000000006" CREATED="1748352093574" MODIFIED="1748352093574">
<node TEXT="AIService" ID="ID_AISERVICE">
<node TEXT="Beschreibung: Zentrale Klasse für KI-Funktionen, z.B. Antwortgenerierung und Regelmanagement."/>
</node>
<node TEXT="Antwortgenerierung" ID="ID_2000000007" CREATED="1748352093574" MODIFIED="1748352093574"/>
<node TEXT="Regelsystem" ID="ID_2000000008" CREATED="1748352093574" MODIFIED="1748352093574"/>
</node>
<node TEXT="Berichtswesen" ID="ID_2000000009" CREATED="1748352093574" MODIFIED="1748352093574">
<node TEXT="ReportManager" ID="ID_REPORTMANAGER">
<node TEXT="Beschreibung: Erstellt und verwaltet Berichte, z.B. PDF-Export und Statusanzeigen."/>
</node>
<node TEXT="PDF-Export" ID="ID_2000000010" CREATED="1748352093574" MODIFIED="1748352093574"/>
<node TEXT="Statusanzeige" ID="ID_2000000011" CREATED="1748352093574" MODIFIED="1748352093574"/>
</node>
<node TEXT="Datenhaltung" ID="ID_2000000012" CREATED="1748352093574" MODIFIED="1748352093574">
<node TEXT="DatabaseManager" ID="ID_DATABASEMANAGER">
<node TEXT="Beschreibung: Kapselt den Zugriff auf die SQLite-Datenbanken je Modul."/>
    def backup(self):
        pass
    def restore(self):
        pass
]]></richcontent>
</node>
</node>
<node TEXT="SQLite je Modul" ID="ID_2000000013" CREATED="1748352093574" MODIFIED="1748352093574"/>
<node TEXT="Backup/Restore" ID="ID_2000000014" CREATED="1748352093574" MODIFIED="1748352093574"/>
</node>
</node>
<node TEXT="Ablauf (Workflow)" ID="ID_2000000015" CREATED="1748352093574" MODIFIED="1748352093574">
<node TEXT="Start" ID="ID_2000000016" CREATED="1748352093574" MODIFIED="1748352093574"/>
<node TEXT="Modulauswahl" ID="ID_2000000017" CREATED="1748352093574" MODIFIED="1748352093574"/>
<node TEXT="Interaktion (z.B. Training, Abfrage)" ID="ID_2000000018" CREATED="1748352093574" MODIFIED="1748352093574"/>
<node TEXT="Bericht erstellen" ID="ID_2000000019" CREATED="1748352093574" MODIFIED="1748352093574"/>
</node>
</node>
</map>

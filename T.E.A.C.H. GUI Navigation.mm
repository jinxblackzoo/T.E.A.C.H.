<map version="freeplane 1.12.1">
<!--To view this file, download free mind mapping software Freeplane from https://www.freeplane.org -->
<node TEXT="T.E.A.C.H. GUI Navigation" LOCALIZED_STYLE_REF="AutomaticLayout.level.root" FOLDED="false" ID="ID_1090958577" CREATED="1409300609620" MODIFIED="1748351670670"><hook NAME="MapStyle" background="#2e3440ff" zoom="0.9090909">
    <properties fit_to_viewport="false" show_icon_for_attributes="true" show_note_icons="true" show_tags="UNDER_NODES" edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" show_icons="BESIDE_NODES" associatedTemplateLocation="template:/dark_nord_template.mm"/>
    <tags category_separator="::"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ID="ID_671184412" ICON_SIZE="12 pt" FORMAT_AS_HYPERLINK="false" COLOR="#484747" BACKGROUND_COLOR="#eceff4" STYLE="bubble" SHAPE_HORIZONTAL_MARGIN="8 pt" SHAPE_VERTICAL_MARGIN="5 pt" BORDER_WIDTH_LIKE_EDGE="false" BORDER_WIDTH="1.9 px" BORDER_COLOR_LIKE_EDGE="true" BORDER_COLOR="#f0f0f0" BORDER_DASH_LIKE_EDGE="true" BORDER_DASH="SOLID">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#88c0d0" WIDTH="2" TRANSPARENCY="255" DASH="" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_671184412" STARTARROW="NONE" ENDARROW="DEFAULT"/>
<font NAME="SansSerif" SIZE="11" BOLD="false" STRIKETHROUGH="false" ITALIC="false"/>
<edge STYLE="bezier" COLOR="#81a1c1" WIDTH="3" DASH="SOLID"/>
<richcontent TYPE="DETAILS" CONTENT-TYPE="plain/auto"/>
<richcontent TYPE="NOTE" CONTENT-TYPE="plain/auto"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details" BORDER_WIDTH="1.9 px">
<edge STYLE="bezier" COLOR="#81a1c1" WIDTH="3"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.tags">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ebcb8b">
<icon BUILTIN="clock2"/>
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.floating" COLOR="#484747">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.selection" COLOR="#e5e9f0" BACKGROUND_COLOR="#5e81ac" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#5e81ac"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.important" ID="ID_779275544" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#bf616a">
<icon BUILTIN="yes"/>
<arrowlink COLOR="#bf616a" TRANSPARENCY="255" DESTINATION="ID_779275544"/>
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.flower" COLOR="#ffffff" BACKGROUND_COLOR="#255aba" STYLE="oval" TEXT_ALIGN="CENTER" BORDER_WIDTH_LIKE_EDGE="false" BORDER_WIDTH="22 pt" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#f9d71c" BORDER_DASH_LIKE_EDGE="false" BORDER_DASH="CLOSE_DOTS" MAX_WIDTH="6 cm" MIN_WIDTH="3 cm"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#ffffff" BACKGROUND_COLOR="#484747" STYLE="bubble" SHAPE_HORIZONTAL_MARGIN="10 pt" SHAPE_VERTICAL_MARGIN="10 pt">
<font NAME="Ubuntu" SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#eceff4" BACKGROUND_COLOR="#d08770" STYLE="bubble" SHAPE_HORIZONTAL_MARGIN="8 pt" SHAPE_VERTICAL_MARGIN="5 pt">
<font NAME="Ubuntu" SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#3b4252" BACKGROUND_COLOR="#ebcb8b">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#2e3440" BACKGROUND_COLOR="#a3be8c">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#2e3440" BACKGROUND_COLOR="#b48ead">
<font SIZE="11"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5" BACKGROUND_COLOR="#81a1c1">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6" BACKGROUND_COLOR="#88c0d0">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7" BACKGROUND_COLOR="#8fbcbb">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8" BACKGROUND_COLOR="#d8dee9">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9" BACKGROUND_COLOR="#e5e9f0">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10" BACKGROUND_COLOR="#eceff4">
<font SIZE="9"/>
</stylenode>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="accessories/plugins/AutomaticLayout.properties" VALUE="ALL"/>
<font BOLD="true"/>
<node TEXT="Die Struktur der Benutzeroberfläche (Navigation) sollte klar von der fachlichen Logik (Funktionalität) getrennt werden. ." LOCALIZED_STYLE_REF="defaultstyle.floating" POSITION="bottom_or_right" ID="ID_819788823" CREATED="1748351664551" MODIFIED="1748351750513" HGAP_QUANTITY="-274.49999 pt" VSHIFT_QUANTITY="-352.49999 pt">
<hook NAME="FreeNode"/>
<node TEXT="Querschnittliche Funktionen wie Einstellungen, Authentifizierung oder KI-Services werden am besten zentral implementiert und von allen Modulen genutzt. So bleibt das System modular, flexibel und leicht wartbar" ID="ID_1450507656" CREATED="1748351708778" MODIFIED="1748351734683"/>
<node TEXT="Diese Trennung fördert Wiederverwendbarkeit und verhindert doppelte Implementierungen." ID="ID_1456539682" CREATED="1748351745871" MODIFIED="1748351747142"/>
</node>
<node TEXT="Hauptmenü (MainMenu)" POSITION="bottom_or_right" ID="ID_1297386687" CREATED="1748292230915" MODIFIED="1748351677737" HGAP_QUANTITY="80.75 pt" VSHIFT_QUANTITY="-3.75 pt">
<node TEXT="Einstellungen (SettingsMenu)" ID="ID_77239798" CREATED="1748292237410" MODIFIED="1748347861738" VSHIFT_QUANTITY="-106.5 pt">
<node TEXT="KI-Einstellungen (AISettingsView)" ID="ID_1566638660" CREATED="1748292346641" MODIFIED="1748347883420">
<node TEXT="Generelle Regeln (GeneralRulesView)" ID="ID_1431043943" CREATED="1748292360567" MODIFIED="1748347909618"/>
<node TEXT="Installation LLM (LLMInstallationView)" ID="ID_404562772" CREATED="1748292370811" MODIFIED="1748347937270"/>
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_1114937813" CREATED="1748292583623" MODIFIED="1748347954104"/>
</node>
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_1615055879" CREATED="1748292583623" MODIFIED="1748347954104"/>
</node>
<node TEXT="Reporting (ReportingMenu)" ID="ID_462344204" CREATED="1748292253792" MODIFIED="1748348031943">
<node TEXT="Report als PDF drucken (ReportPDFView)" ID="ID_186786418" CREATED="1748292703373" MODIFIED="1748345782098" HGAP_QUANTITY="31.25 pt" VSHIFT_QUANTITY="16.5 pt">
<node TEXT="PDF Generierung mit Eingabe des Reportzeitraums (ReportPeriodInputView)" ID="ID_1843146161" CREATED="1748292743525" MODIFIED="1748350829357">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_1029482018" CREATED="1748292583623" MODIFIED="1748292637644"/>
<node TEXT="Eingabe des Zeitraums (PeriodInputView)" ID="ID_1586192382" CREATED="1748292848237" MODIFIED="1748292857364" HGAP_QUANTITY="36.5 pt" VSHIFT_QUANTITY="48 pt"/>
</node>
<node TEXT="PDF Generierung nach Kalenderwoche - Alle KW seit Beginn des aktuellen Jahres (ReportByCalendarWeekView)" ID="ID_787049154" CREATED="1748292778737" MODIFIED="1748292830123"/>
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_492069015" CREATED="1748292583623" MODIFIED="1748347954104"/>
</node>
<node TEXT="Anzeige des aktuellen Status (StatusDisplayView)" ID="ID_498407180" CREATED="1748292892865" MODIFIED="1748345778681" VSHIFT_QUANTITY="47.25 pt">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_1059510517" CREATED="1748292583623" MODIFIED="1748292637644"/>
<node TEXT="Reportanzeige der letzten 7 Tage und 365 Tage (Last7And365DaysView)" ID="ID_1144859880" CREATED="1748293541901" MODIFIED="1748346217321"/>
</node>
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_53257003" CREATED="1748292583623" MODIFIED="1748347954104"/>
</node>
<node TEXT="Module (ModulesMenu)" ID="ID_200486091" CREATED="1748292264768" MODIFIED="1748345766270" VSHIFT_QUANTITY="167.99999 pt">
<node TEXT="VOLL Vokabeltrainer (VOLLModuleView)" ID="ID_505308002" CREATED="1748292273288" MODIFIED="1748346628268" HGAP_QUANTITY="7.25 pt" VSHIFT_QUANTITY="-133.5 pt">
<node TEXT="Zurück zum Hauptmenü (BackButton)" ID="ID_1995292187" CREATED="1748292461790" MODIFIED="1748292470178"/>
<node TEXT="&quot;Existierende Datenbanken&quot; (VOLLDatabaseManagerView)" ID="ID_75731915" CREATED="1748292482523" MODIFIED="1748292496434">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_316577338" CREATED="1748292583623" MODIFIED="1748292637644"/>
<node TEXT="Datenbank bearbeiten (EditCollectionView)" ID="ID_1994110723" CREATED="1748346703002" MODIFIED="1748346922600">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_223654692" CREATED="1748346713683" MODIFIED="1748346715395"/>
<node TEXT="Auflistung aler Sammlungen mit der Möglichkeit zum Umbenennen oder Löschen der ganzen Sammlung (CollectionRenameDeleteView)" ID="ID_1159660981" CREATED="1748346716017" MODIFIED="1748346746456"/>
<node TEXT="KI-Regeln (VOLLRulesView)" POSITION="bottom_or_right" ID="ID_1731954521" CREATED="1748346257215" MODIFIED="1748346264847">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_1440800884" CREATED="1748346265389" MODIFIED="1748346266895"/>
<node TEXT="Eingabe von KI Regeln für die Abfrage und Unterstützung in VOLL (RuleInputView)" ID="ID_1647047316" CREATED="1748346267290" MODIFIED="1748346936997"/>
</node>
<node TEXT="Neue Datenbank erstellen (CreateDatabaseView)" POSITION="bottom_or_right" ID="ID_1334165823" CREATED="1748345947403" MODIFIED="1748346949914">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_529191538" CREATED="1748345979298" MODIFIED="1748345981455"/>
<node TEXT="Eingabe Name der Karteikarten Sammlung (CollectionNameInputView)" ID="ID_99211389" CREATED="1748345982762" MODIFIED="1748346793376"/>
</node>
</node>
</node>
<node TEXT="Beispielsammlung 1 (VOLLExampleCollectionView)" ID="ID_504280140" CREATED="1748346033004" MODIFIED="1748346044884">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_644541029" CREATED="1748346145593" MODIFIED="1748346147675"/>
<node TEXT="Üben (VOLLPracticeView)" ID="ID_579535599" CREATED="1748346068886" MODIFIED="1748346072902">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_544107847" CREATED="1748346225855" MODIFIED="1748346227679"/>
<node TEXT="Übungsabfrage (PracticeQueryView)" ID="ID_40815135" CREATED="1748346228295" MODIFIED="1748346235295"/>
<node TEXT="Chat mit KI für Nachfragen und bei Verständnisschwierigkeiten (VOLLChatView)" ID="ID_1620964597" CREATED="1748346293832" MODIFIED="1748346330724"/>
</node>
<node TEXT="Karteikarten eingeben/bearbeiten (VOLLEditCardsView)" ID="ID_546980668" CREATED="1748346080034" MODIFIED="1748347038068">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_319013818" CREATED="1748346142691" MODIFIED="1748347038068" HGAP_QUANTITY="14.75 pt"/>
<node TEXT="Dokument für KI Unterstützung einlesen (KI soll aus dem Dokument selbstständig Vokabeln erstellen) (DocumentImportView)" ID="ID_1013860681" CREATED="1748346113565" MODIFIED="1748347050995"/>
<node TEXT="Vokabeln händisch eingeben (ManualVocabInputView)" ID="ID_1317773240" CREATED="1748346129052" MODIFIED="1748347018894"/>
<node TEXT="Anzeige der Vokabeln nach Zeitpunkt der Eingabe sortiert mit der Möglichkeit sie zu bearbeiten und der Anzeige wie oft sie bereits bearbeitet/geübt wurden (VocabListView)" POSITION="bottom_or_right" ID="ID_1778660794" CREATED="1748346384547" MODIFIED="1748347027698" HGAP_QUANTITY="16.25 pt" VSHIFT_QUANTITY="0.75 pt"/>
</node>
</node>
<node TEXT="Beispielsammlung 2 (VOLLExampleCollection2View)" ID="ID_433695776" CREATED="1748346045424" MODIFIED="1748346051225"/>
</node>
<node TEXT="MUT Einheitentrainer (MUTModuleView)" ID="ID_1098834041" CREATED="1748292279727" MODIFIED="1748346633911" VSHIFT_QUANTITY="-83.25 pt">
<node TEXT="Zurück zum Hauptmenü (BackButton)" ID="ID_1652373241" CREATED="1748292461790" MODIFIED="1748292470178"/>
<node TEXT="Auswahl der Einheitenrechnungen (MUTUnitSelectionView)" ID="ID_820240412" CREATED="1748345855686" MODIFIED="1748345866024">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_509959602" CREATED="1748345915082" MODIFIED="1748345916588"/>
<node TEXT="Training (MUTTrainingView)" ID="ID_1964663024" CREATED="1748345885214" MODIFIED="1748345896119"/>
<node TEXT="Chat mit KI für Nachfragen und bei Verständnisschwierigkeiten (MUTChatView)" ID="ID_344805052" CREATED="1748346293832" MODIFIED="1748346330724"/>
</node>
</node>
<node TEXT="KLAR Karteikartentrainer (KLARModuleView)" ID="ID_234904161" CREATED="1748292304471" MODIFIED="1748345763206" VSHIFT_QUANTITY="62.25 pt">
<node TEXT="Zurück zum Hauptmenü (BackButton)" ID="ID_777107547" CREATED="1748292461790" MODIFIED="1748292470178"/>
<node TEXT="Beispielsammlung 1 (KLARExampleCollectionView)" POSITION="bottom_or_right" ID="ID_1776549306" CREATED="1748346033004" MODIFIED="1748346044884">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_1743036955" CREATED="1748346145593" MODIFIED="1748346147675"/>
<node TEXT="Üben (KLARPracticeView)" ID="ID_1374652363" CREATED="1748346068886" MODIFIED="1748346072902">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_1201668287" CREATED="1748346225855" MODIFIED="1748346227679"/>
<node TEXT="Übungsabfrage (PracticeQueryView)" ID="ID_1002800697" CREATED="1748346228295" MODIFIED="1748346235295"/>
<node TEXT="Chat mit KI für Nachfragen und bei Verständnisschwierigkeiten (KLARChatView)" ID="ID_919719682" CREATED="1748346293832" MODIFIED="1748346330724"/>
</node>
<node TEXT="Karteikarten eingeben/bearbeiten (KLAREditCardsView)" ID="ID_1873691000" CREATED="1748346080034" MODIFIED="1748346529983">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_1640840102" CREATED="1748346142691" MODIFIED="1748346536842" HGAP_QUANTITY="18.5 pt"/>
<node TEXT="Dokument für KI Unterstützung einlesen (KI soll aus dem Dokument selbstständig Karteikarten erstellen) (DocumentImportView)" ID="ID_448072028" CREATED="1748346113565" MODIFIED="1748346369452"/>
<node TEXT="Karteikarten händisch eingeben (ManualCardInputView)" ID="ID_945368327" CREATED="1748346129052" MODIFIED="1748346141529"/>
<node TEXT="Anzeige der Karteikarten nach Zeitpunkt der Eingabe sortiert mit der Möglichkeit sie zu bearbeiten und der Anzeige wie oft sie bereits bearbeitet/geübt wurden (CardListView)" POSITION="bottom_or_right" ID="ID_1403825580" CREATED="1748346384547" MODIFIED="1748346529983" HGAP_QUANTITY="16.25 pt" VSHIFT_QUANTITY="0.75 pt"/>
</node>
</node>
<node TEXT="Beispielsammlung 2 (KLARExampleCollection2View)" POSITION="bottom_or_right" ID="ID_1105407221" CREATED="1748346045424" MODIFIED="1748346051225"/>
<node TEXT="Karteikarten-Sammlung verwalten (KLARCollectionManagementView)" POSITION="bottom_or_right" ID="ID_1452840495" CREATED="1748346703002" MODIFIED="1748346713240">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_954527663" CREATED="1748346713683" MODIFIED="1748346715395"/>
<node TEXT="Auflistung aler Sammlungen mit der Möglichkeit zum Umbenennen oder Löschen der ganzen Sammlung (CollectionRenameDeleteView)" ID="ID_1265696988" CREATED="1748346716017" MODIFIED="1748346746456"/>
<node TEXT="KI-Regeln (KLARRulesView)" POSITION="bottom_or_right" ID="ID_1601526705" CREATED="1748346257215" MODIFIED="1748346264847">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_48429027" CREATED="1748346265389" MODIFIED="1748346266895"/>
<node TEXT="Eingabe von KI Regeln für die Abfrage und Unterstützung in KLAR (RuleInputView)" ID="ID_455807739" CREATED="1748346267290" MODIFIED="1748346609431"/>
</node>
<node TEXT="Neue Karteikarten-Sammlung erstellen (CreateCollectionView)" POSITION="bottom_or_right" ID="ID_777004301" CREATED="1748345947403" MODIFIED="1748345962098">
<node TEXT="Zurück ins vorherige Menü (BackButton)" ID="ID_1919554402" CREATED="1748345979298" MODIFIED="1748345981455"/>
<node TEXT="Eingabe Name der Karteikarten Sammlung (CollectionNameInputView)" ID="ID_1189104571" CREATED="1748345982762" MODIFIED="1748346793376"/>
</node>
</node>
</node>
</node>
</node>
</node>
</map>

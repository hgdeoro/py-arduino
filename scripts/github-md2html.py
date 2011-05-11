#!/usr/bin/python
# -*- coding: utf-8

import BaseHTTPServer
import codecs
import markdown
import sys

class H(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_GET(self):
        print self.path
        if self.path == '/':
            input_file = codecs.open(sys.argv[1], mode="r", encoding="utf8")
            mdtext = input_file.read()
            input_file.close()
            
            html = markdown.Markdown().convert(mdtext)
            self.end_headers()
            self.wfile.write("""<html><head>
                <link href="bundle_github.css" media="screen"  rel="stylesheet" type="text/css" />
                </head><body class="logged_in page-blob  linux env-production">
                <div class="subnavd" id="main"> 
                <div class="site"> 
                <div class="slider"> 
                <div class="frames"> 
                <div class="frame frame-center"> 
                <div id="files"> 
                <div class="file"> 
                <div class="blob instapaper_body"> 
                <div class="wikistyle"> 
            """)
            
            self.wfile.write(html)
            
            self.wfile.write("""
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </body></html>
            """)
        
        elif self.path == '/bundle_github.css':
            self.end_headers()
            self.wfile.write("""
.ac_results{padding:0;border:1px solid WindowFrame;background-color:Window;overflow:hidden;z-index:1000;}
.ac_results ul{list-style-position:outside;list-style:none;padding:0;margin:0;}
.ac_results li{margin:0;padding:2px 5px;cursor:default;display:block;font:menu;font-size:12px;overflow:hidden;text-align:left;}
.ac_loading{background:Window url('/images/modules/ajax/indicator.gif') right center no-repeat;}
.ac_over{background-color:Highlight;color:HighlightText;text-align:left;}
.date_selector,.date_selector *{width:auto;height:auto;border:none;background:none;margin:0;padding:0;text-align:left;text-decoration:none;}
.date_selector{-webkit-box-shadow:0 0 13px rgba(0,0,0,0.31);-moz-box-shadow:0 0 13px rgba(0,0,0,0.31);background:#fff;border:1px solid #c1c1c1;padding:5px;margin-top:10px;z-index:9;width:240px;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;display:none;}
.date_selector.no_shadow{-webkit-box-shadow:none;-moz-box-shadow:none;}
.date_selector_ieframe{position:absolute;z-index:99999;display:none;}
.date_selector .nav{width:17.5em;}
.date_selector .month_nav,.date_selector .year_nav{margin:0 0 3px 0;padding:0;display:block;position:relative;text-align:center;}
.date_selector .month_nav{float:left;width:55%;}
.date_selector .year_nav{float:right;width:35%;margin-right:-8px;}
.date_selector .month_name,.date_selector .year_name{font-weight:bold;line-height:20px;}
.date_selector .button{display:block;position:absolute;top:0;width:18px;height:18px;line-height:17px;font-weight:bold;color:#003C78;text-align:center;font-size:120%;overflow:hidden;border:1px solid #F2F2F2;}
.date_selector .button:hover,.date_selector .button.hover{background:none;color:#003C78;cursor:pointer;border-color:#ccc;}
.date_selector .prev{left:0;}
.date_selector .next{right:0;}
.date_selector table{border-spacing:0;border-collapse:collapse;clear:both;}
.date_selector th,.date_selector td{width:2.5em;height:2em;padding:0;text-align:center;color:black;}
.date_selector td{border:1px solid #ccc;line-height:2em;text-align:center;white-space:nowrap;color:#003C78;background:white;}
.date_selector td.today{background:#FFFEB3;}
.date_selector td.unselected_month{color:#ccc;}
.date_selector td.selectable_day{cursor:pointer;}
.date_selector td.selected{background:#D8DFE5;font-weight:bold;}
.date_selector td.selectable_day:hover,.date_selector td.selectable_day.hover{background:#003C78;color:white;}
#facebox{position:absolute;top:0;left:0;z-index:100;text-align:left;}
#facebox .popup{position:relative;border:3px solid rgba(0,0,0,0);-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;-webkit-box-shadow:0 0 18px rgba(0,0,0,0.4);-moz-box-shadow:0 0 18px rgba(0,0,0,0.4);box-shadow:0 0 18px rgba(0,0,0,0.4);}
#facebox .content{min-width:370px;padding:10px;background:#fff;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
#facebox .content>p:first-child{margin-top:0;}
#facebox .content>p:last-child{margin-bottom:0;}
#facebox .close{position:absolute;top:5px;right:5px;padding:2px;}
#facebox .close img{opacity:.3;}
#facebox .close:hover img{opacity:1.0;}
#facebox .loading{text-align:center;}
#facebox .image{text-align:center;}
#facebox img{border:0;margin:0;}
#facebox_overlay{position:fixed;top:0;left:0;height:100%;width:100%;}
.facebox_hide{z-index:-100;}
.facebox_overlayBG{background-color:#000;z-index:99;}
.tipsy{padding:5px;font-size:11px;text-shadow:1px 1px 0 #000;opacity:.8;filter:alpha(opacity=80);background-repeat:no-repeat;}
.tipsy-inner{padding:5px 8px 4px 8px;background-color:black;color:white;max-width:235px;text-align:center;-moz-border-radius:3px;-webkit-border-radius:3px;}
.tipsy-north{background-image:url(/images/modules/tipsy/tipsy-north.gif);background-position:top center;}
.tipsy-south{background-image:url(/images/modules/tipsy/tipsy-south.gif);background-position:bottom center;}
.tipsy-east{background-image:url(/images/modules/tipsy/tipsy-east.gif);background-position:right center;}
.tipsy-west{background-image:url(/images/modules/tipsy/tipsy-west.gif);background-position:left center;}
.tipsy-west .tipsy-inner{text-align:left;}
.accountcols .main{float:left;width:560px;}
.accountcols .sidebar{float:right;width:330px;}
.accountcols .main>p.overview{margin-top:20px;color:#333;}
.lineoption{margin:15px 0 25px 0;}
.lineoption h3{margin-bottom:0;font-size:16px;}
.lineoption p{margin:0 0 15px 0;color:#333;}
.statgroup{margin:10px 0;font-size:12px;color:#333;}
.statgroup dl{padding:3px 0;border-bottom:1px solid #ddd;}
.statgroup dl:first-child{border-top:1px solid #ddd;}
.statgroup dl dt{float:left;width:80px;color:#999;}
.statgroup dl dd.action{float:right;font-weight:bold;}
.statgroup ul.actions,.usagebars ul.actions{margin:5px 0;}
.statgroup ul.actions:after,.usagebars ul.actions:after{content:".";display:block;height:0;clear:both;visibility:hidden;}
* html .statgroup ul.actions,* html .usagebars ul.actions{height:1%;}
.statgroup ul.actions,.usagebars ul.actions{display:inline-block;}
.statgroup ul.actions,.usagebars ul.actions{display:block;}
.statgroup ul.actions li,.usagebars ul.actions li{list-style-type:none;margin:0;height:25px;font-weight:bold;}
.statgroup ul.actions li.first,.usagebars ul.actions li.first{float:left;line-height:25px;}
.statgroup ul.actions li.last,.usagebars ul.actions li.last{float:right;}
.fieldgroup p.explain.planusage{color:#333;}
.fieldgroup p.explain.planusage strong{color:#000;}
.usagebars{margin-top:10px;}
.usagebars dl{margin:0;padding:6px 0 8px 0;font-size:12px;color:#999;border-bottom:1px solid #ddd;}
.usagebars dl:first-child{border-top:1px solid #ddd;}
.htabs .usagebars dl{border:none;}
.usagebars dl dt{float:left;}
.usagebars dl dt.numbers{float:right;color:#000;font-weight:bold;}
.usagebars dl dt.numbers em{font-style:normal;color:#999;}
.usagebars dl.reaching dt.numbers em{color:#cd8700;}
.usagebars dl.over dt.numbers em{color:#c00;}
.usagebars dl dt.numbers .overlimit{display:inline-block;position:relative;top:-1px;padding:2px 15px 1px 5px;font-size:9px;font-weight:bold;text-transform:uppercase;text-shadow:1px 1px 0 #804b00;color:#fff;background:url(/images/modules/account/flag_point.png) 100% 50% no-repeat #d55500;-webkit-border-radius:3px;-moz-border-radius:3px;}
.usagebars dl dd{clear:both;}
.usagebars dl dd.bar{border:2px solid #ddd;}
.usagebars dl dd.bar span{display:block;height:20px;min-width:2px;text-indent:-9999px;background:url(/images/modules/account/usage_bars.gif) 0 0 repeat-x;}
.usagebars dl.reaching dd.bar span{background-position:0 -20px;}
.usagebars dl.over dd.bar span{background-position:0 -40px;}
.usagebars .ssl{display:inline-block;padding-left:20px;font-size:12px;font-weight:normal;color:#999;background:url(/images/modules/account/ssl_icons.gif) 0 0 no-repeat;}
.usagebars .ssl.disabled{background-position:0 -30px;}
.usagebars p.upsell{margin:0;padding:5px 0;font-size:12px;font-weight:bold;text-align:center;border-bottom:1px solid #ddd;}
ul.usagestats{margin:10px 0 10px -30px;width:950px;}
ul.usagestats li{list-style-type:none;float:left;margin:0 0 0 30px;width:230px;}
ul.usagestats li.name{width:140px;}
.usagestats dl,.usagestats dl:first-child{padding:0;border:none;}
.usagestats dl dt{float:none;}
.usagestats dl dt.numbers{position:relative;float:none;font-size:20px;font-weight:bold;color:#000;}
.usagestats dl dt.numbers em{color:#666;}
.usagestats dl dt.numbers .overlimit{position:absolute;top:12px;right:235px;padding-top:4px;padding-bottom:3px;white-space:nowrap;line-height:1;}
.usagestats dl dt.numbers .suffix{font-size:18px;}
.usagestats dl dt.label{margin:-6px 0 5px 0;text-transform:lowercase;}
#planchange .fieldgroup{margin-top:0;}
#planchange .fieldgroup .fields{background-image:url(/images/modules/account/fieldgroup_back-blue.gif);}
#just_change_plan{float:right;margin-top:2px;}
#planchange ul.warnings{list-style-type:none;}
#planchange ul.warnings li{color:#900;font-weight:bold;font-size:14px;}
table.upgrades{margin:0;width:100%;border-spacing:0;border-collapse:collapse;}
table.upgrades#org_plans{margin:10px 0 15px 0;border-top:1px solid #ddd;}
table.upgrades th{padding:4px 5px;text-align:left;font-size:11px;font-weight:normal;color:#666;border-bottom:1px solid #ddd;}
table.upgrades th .private-icon{display:inline-block;width:8px;height:9px;text-indent:-9999px;background:url(/images/modules/account/table_lock.png) 0 0 no-repeat;}
table.upgrades td{padding:8px 5px;font-size:16px;font-weight:bold;border-bottom:1px solid #ddd;background:url(/images/modules/account/billing_bevel.gif) 0 0 repeat-x #f5f5f5;}
table.upgrades td.upsell{padding:5px;font-size:12px;color:#555;}
table.upgrades td.upsell a{font-weight:bold;}
table.upgrades tr:hover td{background-color:#d2f4f4;}
table.upgrades tr.selected td{background-color:#333;color:#fff;}
table.upgrades tr.current td{background-color:#fdffce;color:#000;}
table.upgrades td.num,table.upgrades td.bool,table.upgrades th.num,table.upgrades th.bool{text-align:center;}
table.upgrades td.action{text-align:right;font-size:11px;color:#999;}
table.upgrades td.name em{font-style:normal;color:#666;}
table.upgrades .coupon td{padding:5px;color:#fff;font-size:11px;}
table.upgrades .coupon td,table.upgrades tr.coupon:hover td{background-color:#df6e00;}
table.upgrades .coupon td.timeleft{font-weight:normal;text-align:right;padding-right:25px;background:url(/images/modules/account/timer.png) 98% 50% no-repeat #df6e00;}
table.upgrades.selected td{padding-top:4px;padding-bottom:4px;opacity:.5;font-size:12px;}
table.upgrades.selected tr.selected td{padding-top:8px;padding-bottom:8px;opacity:1.0;font-size:16px;}
.creditcard{padding-left:60px;background:url(/images/modules/account/credit_card.gif) 0 3px no-repeat;}
.creditcard.invalid{background-position:0 -47px;}
.creditcard h3{margin:0;font-size:14px;}
.creditcard.invalid h3{color:#900;}
.creditcard h3 .update{position:relative;top:-2px;margin-left:10px;}
.creditcard p{margin:-5px 0 0 0;font-size:12px;font-weight:bold;}
table.notifications{margin:0 0 15px 0;width:100%;border-spacing:none;border-collapse:collapse;font-size:12px;color:#666;}
table.notifications th{padding:15px 0 5px 0;text-align:left;font-size:11px;text-transform:uppercase;color:#000;border-bottom:1px solid #ccc;}
table.notifications td{padding:2px 0;border-bottom:1px solid #ddd;}
table.notifications td.checkbox{width:1%;text-align:center;}
p.notification-settings{margin:15px 0;padding-left:20px;font-size:12px;color:#333;background:url(/images/modules/notifications/notification_icon.png) 0 50% no-repeat;}
p.notification-settings.ignored{background-image:url(/images/modules/notifications/notification_icon-off.png);}
p.notification-settings strong{font-weight:bold;}
p.notification-settings em{font-style:normal;color:#666;}
.page-notifications p.notification-settings{margin-bottom:0;padding:8px 5px 8px 25px;background-color:#eee;background-position:5px 50%;border:1px solid #d5d5d5;border-right-color:#e5e5e5;border-bottom-color:#e5e5e5;-webkit-border-radius:3px;-moz-border-radius:3px;}
p.notification-settings label{margin-right:5px;}
.payment-type{margin:15px 0 10px 0;padding:0 0 15px 0;border-bottom:1px solid #ddd;}
.payment-type ul.actions{margin:0;float:right;}
.payment-type ul.actions li{list-style-type:none;float:right;margin:0 0 0 10px;height:25px;line-height:25px;font-size:11px;color:#999;}
.payment-type h3{margin:0;height:25px;line-height:24px;font-size:14px;}
.payment-type.gift h3,.payment-type.nonprofit h3,.payment-type.teacher h3,.payment-type.student h3{padding-left:26px;background:url(/images/modules/account/payment-gift.png) 0 50% no-repeat;}
.payment-type.card h3{padding-left:40px;background:url(/images/modules/account/payment-card.png) 0 50% no-repeat;}
.payment-type.invoice h3{padding-left:25px;background:url(/images/modules/account/payment-invoice.png) 0 50% no-repeat;}
.payment-type.coupon h3{padding-left:35px;background:url(/images/modules/account/payment-coupon.png) 0 50% no-repeat;}
#facebox .content.job-profile-preview{width:500px;}
#admin_bucket form.edit_user p{margin:10px 0 5px 0;}
.site{margin:0 auto;width:920px;padding:0 15px;}
#header{border-bottom:none;margin-bottom:0;}
#header.basic{margin-bottom:20px;}
h2,h3{margin:1em 0;}
.sidebar h4{margin:15px 0 5px 0;font-size:11px;color:#666;text-transform:uppercase;}
.file{margin:15px 0;}
.file>.highlight{padding:5px;background:#f8f8ff;border:1px solid #d4d4e3;}
.file>h3{margin:0;padding:5px;font-size:12px;color:#333;text-shadow:1px 1px 0 rgba(255,255,255,0.5);border:1px solid #ccc;border-bottom:none;background:url(/images/modules/commit/file_head.gif) 0 0 repeat-x #eee;}
.blob-editor textarea{font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:11px;}
dl.form{margin:15px 0;}
.fieldgroup dl.form:first-child{margin-top:0;}
dl.form dt{margin:0;font-size:14px;font-weight:bold;color:#333;}
dl.form.required dt label{padding-right:8px;background:100% 0 no-repeat url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAAHCAYAAADEUlfTAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyJpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBNYWNpbnRvc2giIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6QjcyQTEwREI1MUI2MTFFMEJEMzA4NTRCMDg2RkMxQjUiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6QjcyQTEwREM1MUI2MTFFMEJEMzA4NTRCMDg2RkMxQjUiPiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDpCNzJBMTBEOTUxQjYxMUUwQkQzMDg1NEIwODZGQzFCNSIgc3RSZWY6ZG9jdW1lbnRJRD0ieG1wLmRpZDpCNzJBMTBEQTUxQjYxMUUwQkQzMDg1NEIwODZGQzFCNSIvPiA8L3JkZjpEZXNjcmlwdGlvbj4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gPD94cGFja2V0IGVuZD0iciI/PvOj8Z8AAABdSURBVHjaYlzMzIAMdgPxaiCeBeIwQQWVoLQLEAtC2cYgyTQgvgvVBQKhQPwOiFexQI2BCYJ1AHEnSByk8z0Q74EKnoUqABl9lglNlysQV8DsZkRyrSDUFDgbIMAAoD8RR3CjLAoAAAAASUVORK5CYII=);}
dl.miniform dt{font-size:12px;}
dl.form dd input[type=text],dl.form dd input[type=password]{margin-right:5px;font-size:14px;width:400px;padding:5px;color:#666;background-repeat:no-repeat;background-position:right center;}
dl.miniform dd input{margin-right:0;font-size:12px;padding:4px;}
.sidebar dl.miniform dd input{width:97%;}
dl.form dd textarea{font-size:12px;width:98%;height:200px;padding:5px;}
dl.form dd textarea.short{height:50px;}
dl.form dd p.note,dl.form dd.required{margin:2px 0 5px 0;font-size:11px;color:#666;}
dl.form dd img{vertical-align:middle;}
dl.form .success{font-size:12px;font-weight:bold;color:#390;}
dl.form .error{font-size:12px;font-weight:bold;color:#900;}
dl.form dd.error{margin:0;display:inline-block;padding:5px;font-size:11px;font-weight:bold;color:#333;background:#f7ea57;border:1px solid #c0b536;border-top:1px solid #fff;-webkit-border-bottom-right-radius:3px;-webkit-border-bottom-left-radius:3px;-moz-border-radius-bottomright:3px;-moz-border-radius-bottomleft:3px;border-bottom-right-radius:3px;border-bottom-left-radius:3px;}
dl.form.card-type{float:left;margin-top:0;margin-right:25px;}
dl.form.expiration{margin-top:0;}
.form-actions .success{color:#390;font-weight:bold;}
dl.form dt label{position:relative;}
dl.form.error dt label{color:#900;}
dl.form.loading{opacity:.5;}
dl.form.loading dt .indicator{position:absolute;top:0;right:-20px;display:block;width:16px;height:16px;background:url(/images/modules/ajax/indicator.gif) 0 0 no-repeat;}
dl.form.success dt .indicator{position:absolute;top:0;right:-20px;display:block;width:16px;height:16px;background:url(/images/modules/ajax/success.png) 0 0 no-repeat;}
dl.form.error dt .indicator{position:absolute;top:0;right:-20px;display:block;width:16px;height:16px;background:url(/images/modules/ajax/error.png) 0 0 no-repeat;}
dl.password-confirmation-form{margin-top:-5px;margin-bottom:0;}
dl.password-confirmation-form dd input[type=password]{width:230px;}
dl.password-confirmation-form button{position:relative;left:-3px;top:-2px;}
.hfields{margin:15px 0;}
.hfields:after{content:".";display:block;height:0;clear:both;visibility:hidden;}
* html .hfields{height:1%;}
.hfields{display:inline-block;}
.hfields{display:block;}
.hfields dl.form{float:left;margin:0 30px 0 0;}
.hfields button.classy,.hfields a.button.classy{float:left;margin:15px 25px 0 -20px;}
.hfields select{margin-top:5px;}
.hfields dl.form dd label{display:inline-block;margin:5px 0 0 15px;color:#666;}
.hfields dl.form dd label:first-child{margin-left:0;}
.hfields dl.form dd label img{position:relative;top:-2px;}
input[type=text].short,dl.form input[type=text].short{width:250px;}
p.checkbox{margin:15px 0;font-size:14px;font-weight:bold;color:#333;}
.ejector{position:relative;margin:15px 0;padding:10px;border:1px solid #dcb5b5;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.ejector.ejecting{padding-right:50px;background:url(/images/icons/bigwarning.png) 98% 50% no-repeat #fffeb2;}
.ejector h3{margin:0;color:#900;}
.ejector p{margin:0;color:#666;}
.ejector p+p{margin-top:15px;}
.ejector p strong.yell{color:#000;background:#fff693;}
.ejector.ejecting p{font-weight:bold;color:#000;}
.ejector button.classy,.ejector .button.classy{position:absolute;top:50%;right:10px;margin-top:-18px;}
.ejector-actions{margin:-5px 0 15px 0;}
.ejector-actions .cancel{font-weight:bold;font-size:11px;}
.ejector-actions button,.ejector-actions .button,.ejector-actions .minibutton{float:right;}
.ejector-content{width:55%;}
.fieldgroup{position:relative;margin-top:10px;}
.sidebar .fieldgroup+.fieldgroup{margin-top:40px;}
.fieldgroup h2,h2.account{margin:15px 0 0 0;font-size:18px;font-weight:normal;color:#666;}
p.explain{font-size:12px;color:#666;}
.fieldgroup p.explain{margin:0;}
.fieldgroup .fields{margin:10px 0 0 0;padding:10px;background:url(/images/modules/account/fieldgroup_back.png) 0 0 no-repeat;}
.equacols .fieldgroup .fields,.htabs .columns.typical .fieldgroup .fields,.htabs .columns.hooks .fieldgroup .fields{background-image:url(/images/modules/account/fieldgroup_back-440.png);}
.fieldgroup p.addlink{margin:15px 0;font-size:14px;font-weight:bold;}
.fieldgroup p.checkbox label{margin-left:5px;}
.fieldgroup p.checkbox .succeed{margin-left:10px;font-weight:normal;color:#3c0;}
.fieldgroup p.danger{margin:15px 0;font-weight:bold;color:#c00;}
.fieldgroup p:first-child{margin-top:0;}
.fieldgroup p.extra{margin:-8px 0 15px 0;font-size:12px;color:#666;}
.fieldgroup p.legal{margin:15px 0;font-size:14px;font-weight:bold;}
.fieldgroup div.error{margin:10px 0 0 0;padding:10px;color:#fff;font-weight:bold;background:#a00;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;-webkit-font-smoothing:antialiased;}
.fieldgroup div.error p{margin:0;}
.fieldgroup div.error p+p{margin-top:10px;}
ul.fieldpills{position:relative;margin:0;}
ul.fieldpills li{position:relative;list-style-type:none;margin:3px 0;min-height:24px;line-height:24px;padding:4px 5px;background:#eee;font-size:12px;font-weight:bold;color:#333;border:1px solid #ddd;-webkit-border-radius:3px;-moz-border-radius:3px;}
ul.fieldpills li:first-child{margin-top:0;}
ul.fieldpills li:hover{background-color:#f5f5f5;border-color:#ccc;}
ul.fieldpills.public_keys li{padding-left:28px;background-image:url(/images/modules/account/public_key.png);background-repeat:no-repeat;background-position:10px 50%;}
ul.fieldpills.teams li{padding-left:28px;background-image:url(/images/icons/team.png);background-repeat:no-repeat;background-position:5px 50%;}
ul.fieldpills li .remove{position:absolute;top:50%;right:10px;margin-top:-9px;width:18px;height:18px;text-indent:-9999px;text-decoration:none;background:url(/images/modules/account/close_pill.png) 0 0 no-repeat;}
ul.fieldpills li .remove:hover{background-position:0 -50px;}
ul.fieldpills li img.remove{background:none;}
ul.fieldpills li .dingus{position:absolute;top:50%;right:10px;margin-top:-9px;text-indent:-9999px;text-decoration:none;}
.avatarexplain{margin:15px 0;height:54px;}
.avatarexplain img{float:left;margin-right:10px;padding:2px;background:#fff;border:1px solid #ddd;}
.avatarexplain p{margin:0;padding-top:10px;font-size:12px;line-height:1;color:#999;}
.avatarexplain p strong{display:block;font-size:14px;font-weight:bold;color:#333;}
.add-pill-form{margin:15px 0;padding:4px 5px;background:#f5f5f5;font-size:12px;color:#333;border:1px solid #ddd;-webkit-border-radius:5px;-moz-border-radius:5px;}
.add-pill-form input[type=text]{font-size:14px;width:350px;padding:2px 5px;color:#666;}
.equacols .add-pill-form input[type=text],.htabs .columns.typical .add-pill-form input[type=text]{width:332px;}
.add-pill-form img{vertical-align:middle;margin:0 5px;}
.add-pill-form .error_box{margin:5px 0 0 0;padding:0;border:none;background:transparent;color:#c00;font-size:12px;}
.add-pill-form label{margin:12px 0 2px 0;display:block;font-weight:bold;color:#333;}
.add-pill-form label:first-child{margin-top:0;}
.add-pill-form textarea.key_value{font-size:11px;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;width:95%;height:120px;}
.add-pill-form .form-actions{margin-top:10px;text-align:left;}
ul.smalltabs{margin:15px 0 15px 0;height:24px;line-height:24px;font-size:12px;color:#555;text-shadow:1px 1px 0 rgba(255,255,255,0.5);background:url(/images/modules/pagehead/breadcrumb_back.gif) 0 0 repeat-x;border:1px solid #d1d1d1;border-bottom-color:#bbb;-webkit-border-radius:3px;-moz-border-radius:3px;}
ul.smalltabs li{list-style-type:none;display:inline;}
ul.smalltabs a{float:left;height:24px;padding:0 7px;line-height:24px;color:#666;font-weight:bold;text-decoration:none;border-right:1px solid #ababab;border-left:1px solid #f6f6f6;}
ul.smalltabs li:first-child a{border-left:none;}
ul.smalltabs a.selected{color:#333;background:url(/images/modules/tabs/small_highlight.gif) 0 0 repeat-x;}
ul.smalltabs li:first-child a.selected{-webkit-border-top-left-radius:3px;-webkit-border-bottom-left-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-bottomleft:3px;border-top-left-radius:3px;border-bottom-left-radius:3px;}
ul.smalltabs .counter{display:inline-block;position:relative;top:-1px;margin-left:2px;padding:1px 3px 0 3px;font-size:9px;background:#ececec;border:1px solid #afafaf;border-right-color:#ececec;border-bottom-color:#ececec;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
ul.smalltabs .counter.green_highlight{background:#cfc;color:#393;}
ul.smalltabs .counter.red_highlight{background:#fcc;color:#933;}
ul.smalltabs .icon{display:inline-block;position:relative;top:4px;width:16px;height:16px;opacity:.5;}
ul.smalltabs a.selected .icon{opacity:1.0;}
ul.smalltabs .discussion-icon{background:url(/images/modules/tabs/icon_discussion.png) 0 0 no-repeat;}
ul.smalltabs .commits-icon{background:url(/images/modules/tabs/icon_commits.png) 0 0 no-repeat;}
ul.smalltabs .fileschanged-icon{background:url(/images/modules/tabs/icon_fileschanged.png) 0 0 no-repeat;}
p.breadcrumb{margin:10px 0 0 0;padding:0 7px;height:24px;line-height:24px;font-size:12px;color:#555;text-shadow:1px 1px 0 rgba(255,255,255,0.5);background:url(/images/modules/pagehead/breadcrumb_back.gif) 0 0 repeat-x;border:1px solid #d1d1d1;border-bottom-color:#bbb;-webkit-border-radius:3px;-moz-border-radius:3px;}
p.breadcrumb a{color:#333;font-weight:bold;}
p.breadcrumb .separator{display:inline-block;margin:-1px 3px 0 3px;height:8px;width:8px;text-indent:-9999px;vertical-align:middle;background:url(/images/modules/pagehead/breadcrumb_separator.png) 0 0 no-repeat;}
.metabox+p.breadcrumb{margin-top:-10px;}
.htabs:after{content:".";display:block;height:0;clear:both;visibility:hidden;}
* html .htabs{height:1%;}
.htabs{display:inline-block;}
.htabs{display:block;}
.htabs{margin:15px 0;border-top:1px solid #ddd;background:url(/images/modules/tabs/side_rule.gif) 230px 0 repeat-y;}
.htabs .tab-content{float:right;width:670px;}
ul.sidetabs{float:left;margin:0;width:229px;}
ul.sidetabs li{list-style-type:none;margin:10px 0;}
ul.sidetabs li a{display:block;padding:8px 10px 7px 10px;font-size:14px;text-decoration:none;border:1px solid transparent;-webkit-border-top-left-radius:4px;-webkit-border-bottom-left-radius:4px;-moz-border-radius-topleft:4px;-moz-border-radius-bottomleft:4px;}
ul.sidetabs li a:hover{border-top-left-radius:4px;border-bottom-left-radius:4px;background:#f1f1f1;}
ul.sidetabs li a.loading{background:url(/images/modules/ajax/indicator.gif) 97% 50% no-repeat;}
ul.sidetabs li a.selected{color:#333;font-weight:bold;text-shadow:1px 1px 0 #fff;border:1px solid #ddd;border-right:none;background:url(/images/modules/tabs/sidebar_selected.gif) 0 0 repeat-x;}
.columns.typical .main{float:left;width:560px;}
.columns.typical .sidebar{float:right;width:330px;}
.htabs .columns.typical .main{width:440px;}
.htabs .columns.typical .sidebar{width:210px;}
.columns.dashcols .main{float:left;width:560px;}
.columns.dashcols .sidebar{float:right;width:337px;}
.columns.equacols .column{width:440px;float:left;}
.columns.equacols .secondary{float:right;}
.columns.equacols.bordered{border-top:1px solid #ddd;border-bottom:1px solid #ddd;background:url(/images/modules/global/column_separator.gif) 50% 0 repeat-y;}
.columns.hooks .sidebar{float:left;width:210px;}
.columns.hooks .main{float:right;width:440px;}
.columns.profilecols .first{float:left;width:450px;}
.columns.profilecols .last{float:right;width:450px;}
.columns.browser .sidebar{float:left;width:220px;padding-right:19px;border-right:1px solid #ddd;}
.columns.browser .main{float:right;width:660px;}
.columns.content-left{background:url(/images/modules/marketing/rule.gif) 670px 0 repeat-y;}
.columns.content-left .main{float:left;width:650px;}
.columns.content-left .sidebar{float:right;width:230px;}
.columns.fourcols .column{float:left;margin-left:20px;width:215px;}
.columns.fourcols .column.leftmost{margin-left:0;}
.wider .columns.content-left{background:url(/images/modules/marketing/rule.gif) 690px 0 repeat-y;}
.wider .columns.content-left .main{float:left;width:670px;}
.wider .columns.content-left .sidebar{float:right;width:248px;}
.wider .feature-content{padding:0 5px;}
.wider .columns.equacols .first{float:left;width:460px;}
.wider .columns.equacols .last{float:right;width:460px;}
.wider .columns.threecols .column{float:left;width:300px;margin-left:24px;}
.wider .columns.threecols .column.first{margin-left:0;}
#impact_legend p,#impact_graph p{margin:0;}
.keyboard-shortcuts{float:right;margin:5px 0 0 0;padding-right:25px;font-size:11px;text-decoration:none;color:#666;background:url(/images/icons/keyboard.png) 100% 50% no-repeat;}
.page-commits .keyboard-shortcuts{margin-top:20px;}
#issues .keyboard-shortcuts{margin-top:10px;margin-right:10px;padding:5px;background-image:none;background-color:#eee;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
#facebox .content.shortcuts{width:700px;}
#facebox .content.shortcuts .columns.equacols .column{width:45%;}
#facebox .content.shortcuts .equacols .last{float:right;}
#facebox .content.shortcuts .columns.threecols .column{float:left;width:32%;}
dl.keyboard-mappings{margin:5px 0;font-size:12px;}
dl.keyboard-mappings dt{display:inline-block;margin:0;padding:3px 6px;min-width:10px;text-align:center;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;background:#333;color:#EEE;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;text-shadow:1px 1px 0 #000;}
dl.keyboard-mappings dt em{padding:0 4px;color:#999;font-style:normal;font-weight:normal;font-size:10px;font-family:Helvetica,Arial,freesans,sans-serif;text-shadow:none;}
dl.keyboard-mappings dd{display:inline;margin:0 0 0 5px;color:#666;}
#facebox .shortcuts h3{margin:0 0 10px 0;font-size:14px;}
pre.copyable-terminal,#facebox pre.copyable-terminal{margin-right:20px;padding:10px;color:#fff;background:#333;border:none;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;overflow:auto;}
.for-copyable-terminal{float:right;}
ol.help-steps,#facebox ol.help-steps{margin:15px 0;color:#666;}
ol.help-steps li{list-style-type:none;margin:15px 0;}
ol.help-steps strong{color:#000;font-weight:bold;}
ol.help-steps p{margin-bottom:5px;}
.chooser-box{padding:0 10px 10px;background:#f1f1f1;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#ffffff',endColorstr='#f1f1f1');background:-webkit-gradient(linear,left top,left bottom,from(#fff),to(#f1f1f1));background:-moz-linear-gradient(top,#fff,#f1f1f1);border:1px solid #ddd;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.chooser-box h3{margin:0 0 0 -10px;width:100%;padding:13px 10px 10px;font-size:16px;line-height:1.2;color:#222;text-shadow:1px 1px 0 rgba(255,255,255,0.5);background:#fbfbfb;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fbfbfb',endColorstr='#f2f2f2');background:-webkit-gradient(linear,left top,left bottom,from(#fbfbfb),to(#f2f2f2));background:-moz-linear-gradient(top,#fbfbfb,#f2f2f2);-webkit-border-top-left-radius:5px;-webkit-border-top-right-radius:5px;-moz-border-radius-topleft:5px;-moz-border-radius-topright:5px;border-top-left-radius:5px;border-top-right-radius:5px;border-bottom:1px solid #fff;}
.chooser-box .fakerule{margin:0 0 0 -10px;width:100%;height:1px;padding:0 10px;font-size:1px;line-height:1px;background:#ddd;}
.chooser-box .ac-accept,.chooser-box .ac_loading{background:inherit;}
.cleanheading h2{font-size:20px;margin:15px 0 15px 0;}
.cleanheading p.subtext{margin:-15px 0 10px 0;color:#666;}
table.branches{margin:5px 0 0 0;width:100%;border-spacing:0;border-collapse:collapse;}
table.branches th{padding:2px 0;font-size:11px;text-transform:uppercase;text-align:left;color:#666;border-bottom:1px solid #ddd;}
table.branches th.state-widget{text-align:center;}
table.branches tr td{padding:5px 0;border-bottom:1px solid #ddd;}
table.branches tr:hover td{background:#fafafa;}
table.branches tr td.state-widget{width:500px;}
table.branches tr.base td{background:#333;color:#fff;}
table.branches tr.base td.name{padding-left:10px;}
table.branches tr.base td.name p{color:#aaa;}
table.branches tr.base td.actions{padding-right:10px;color:#eee;}
.branches .name h3{margin:0;font-size:16px;}
.branches .name p{margin:-3px 0 0 0;font-size:12px;color:#666;}
.branches .state{display:inline-block;margin-right:5px;padding:2px 5px;font-size:11px;text-transform:uppercase;font-weight:bold;background:#eee;-webkit-border-radius:2px;-moz-border-radius:2px;}
.branches .state-progress{font-size:12px;color:#666;font-style:normal;}
.branches ul.actions{float:right;}
.branches ul.actions>li{list-style-type:none;display:inline-block;margin:0 0 0 5px;}
.branches ul.actions>li.text{padding:5px 0;font-size:11px;font-weight:bold;}
.diverge-widget{position:relative;height:35px;}
.diverge-widget .ahead{display:block;position:absolute;width:50%;height:100%;left:50%;}
.diverge-widget .behind{display:block;position:absolute;width:50%;height:100%;right:50%;}
.diverge-widget .bar{position:absolute;top:13px;right:0;display:block;height:8px;background:#d0d0d0;}
.diverge-widget .ahead .bar{background:#7a7a7a;left:0;}
.diverge-widget.hot .bar{background-color:#ff704f;}
.diverge-widget.hot .ahead .bar{background-color:#811201;}
.diverge-widget.fresh .bar{background-color:#ffd266;}
.diverge-widget.fresh .ahead .bar{background-color:#b69e67;}
.diverge-widget.stale .bar{background-color:#b2d0dd;}
.diverge-widget.stale .ahead .bar{background-color:#1e4152;}
.diverge-widget em{font-style:normal;font-size:10px;line-height:10px;color:#999;white-space:nowrap;}
.diverge-widget .behind em{position:absolute;bottom:0;right:5px;}
.diverge-widget .ahead em{position:absolute;top:0;left:5px;}
.diverge-widget .separator{display:block;position:absolute;top:0;left:50%;margin-left:-2px;width:2px;height:100%;background:#454545;}
ul.hotness-legend{float:right;margin:10px 0 0 0;}
ul.hotness-legend li{list-style-type:none;float:left;margin:0;font-size:11px;color:#999;}
ul.hotness-legend .ahead,ul.hotness-legend .behind{display:block;margin:1px 0 0 0;width:15px;height:10px;}
ul.hotness-legend .old .behind{background-color:#d0d0d0;}
ul.hotness-legend .old .ahead{background-color:#7a7a7a;}
ul.hotness-legend .stale .behind{background-color:#b2d0dd;}
ul.hotness-legend .stale .ahead{background-color:#1e4152;}
ul.hotness-legend .fresh .behind{background-color:#ffd266;}
ul.hotness-legend .fresh .ahead{background-color:#b69e67;}
ul.hotness-legend .hot .behind{background-color:#ff704f;}
ul.hotness-legend .hot .ahead{background-color:#811201;}
ul.hotness-legend li.text{margin:0 10px;height:23px;line-height:23px;}
.form-actions{text-align:right;padding-bottom:5px;padding-right:2px;}
.form-actions .cancel{margin-top:5px;float:left;}
.form-actions .button.cancel{margin-top:0;margin-left:2px;}
.form-actions .minibutton.cancel{margin-top:0;}
.form-actions .optional{display:block;padding-top:8px;float:left;margin-right:15px;}
.form-actions .optional span.text{padding:0 3px;}
.form-actions .optional input{position:relative;top:-1px;}
.form-warning{margin:10px 0;padding:8px 5px;border:1px solid #ddd;border-left:none;border-right:none;font-size:14px;color:#333;background:#ffffe2;}
.form-warning p{margin:0;line-height:1.5;}
.form-warning strong{color:#000;}
.form-warning a{font-weight:bold;}
button.classy,a.button.classy,button.classy:disabled:hover,a.button.classy.disabled:hover{height:34px;padding:0;position:relative;top:1px;margin-left:10px;font-family:helvetica,arial,freesans,clean,sans-serif;font-weight:bold;font-size:12px;color:#333;text-shadow:1px 1px 0 #fff;white-space:nowrap;border:none;overflow:visible;background:#ddd;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#ffffff',endColorstr='#e1e1e1');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fff),to(#e1e1e1));background:-moz-linear-gradient(-90deg,#fff,#e1e1e1);border-bottom:1px solid #ebebeb;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;-webkit-box-shadow:0 1px 4px rgba(0,0,0,0.3);-moz-box-shadow:0 1px 4px rgba(0,0,0,0.3);box-shadow:0 1px 4px rgba(0,0,0,0.3);cursor:pointer;-webkit-font-smoothing:subpixel-antialiased!important;}
a.button.classy{display:inline-block;}
button.classy span,a.button.classy span{display:block;height:34px;padding:0 13px;line-height:36px;}
button.classy.glowing,a.button.classy.glowing,button.classy.glowing:disabled:hover,a.button.classy.disabled.glowing:hover{background:#e6e1c0;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fffad5',endColorstr='#e6e1c0');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fffad5),to(#e6e1c0));background:-moz-linear-gradient(-90deg,#fffad5,#e6e1c0);border-bottom-color:#ecead5;}
button.classy.silver,a.button.classy.silver,button.classy.silver:disabled:hover,a.button.classy.disabled.silver:hover{color:#000;text-shadow:1px 1px 0 rgba(255,255,255,0.5);background:#c7c7c7;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fdfdfd',endColorstr='#9a9a9a');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fdfdfd),to(#9a9a9a));background:-moz-linear-gradient(-90deg,#fdfdfd,#9a9a9a);border-bottom-color:#c7c7c7;}
button.classy.silver:hover,a.button.classy.silver:hover{color:#000;text-shadow:1px 1px 0 rgba(255,255,255,0.5);background:#f7f7f7;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#ffffff',endColorstr='#eeeeee');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fff),to(#eee));background:-moz-linear-gradient(-90deg,#fff,#eee);border-bottom-color:#f7f7f7;-webkit-box-shadow:0 1px 4px rgba(255,255,255,0.3);-moz-box-shadow:0 1px 4px rgba(255,255,255,0.3);box-shadow:0 1px 4px rgba(255,255,255,0.3);}
button.classy.silver:disabled:hover,a.button.classy.disabled.silver:hover{-webkit-box-shadow:0 1px 4px rgba(0,0,0,0.3);-moz-box-shadow:0 1px 4px rgba(0,0,0,0.3);box-shadow:0 1px 4px rgba(0,0,0,0.3);}
button.classy.business-plan,a.button.classy.business-plan{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);background:#3e9533;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#419b36',endColorstr='#357f2c');background:-webkit-gradient(linear,0% 0,0% 100%,from(#419b36),to(#357f2c));background:-moz-linear-gradient(-90deg,#419b36,#357f2c);border-bottom-color:#3e9533;}
button.classy.business-plan:hover,a.button.classy.business-plan:hover{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);background:#18a609;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#1cbe0a',endColorstr='#158f07');background:-webkit-gradient(linear,0% 0,0% 100%,from(#1cbe0a),to(#158f07));background:-moz-linear-gradient(-90deg,#1cbe0a,#158f07);border-bottom-color:#18a609;}
button.classy.personal-plan,a.button.classy.personal-plan{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);background:#438bb1;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#4794bc',endColorstr='#3a7999');background:-webkit-gradient(linear,0% 0,0% 100%,from(#4794bc),to(#3a7999));background:-moz-linear-gradient(-90deg,#4794bc,#3a7999);border-bottom-color:#438bb1;}
button.classy.danger:disabled:hover,a.button.classy.disabled.danger:hover{background:#ddd;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#ffffff',endColorstr='#e1e1e1');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fff),to(#e1e1e1));background:-moz-linear-gradient(-90deg,#fff,#e1e1e1);border-bottom:1px solid #ebebeb;color:#900;text-shadow:1px 1px 0 #fff;}
button.classy.danger:hover,a.button.classy.danger:hover{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);background:#b33630;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#dc5f59',endColorstr='#b33630');background:-webkit-gradient(linear,0% 0,0% 100%,from(#dc5f59),to(#b33630));background:-moz-linear-gradient(-90deg,#dc5f59,#b33630);border-bottom-color:#cd504a;}
button.classy.danger.mousedown,a.button.classy.danger.mousedown{background:#b33630;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#b33630',endColorstr='#dc5f59');background:-webkit-gradient(linear,0% 0,0% 100%,from(#b33630),to(#dc5f59));background:-moz-linear-gradient(-90deg,#b33630,#dc5f59);border-bottom-color:#dc5f59;}
button.classy.oauth,a.button.classy.oauth,.login_form form .submit_btn input{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);background:#438bb1;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#4794bc',endColorstr='#3a7999');background:-webkit-gradient(linear,0% 0,0% 100%,from(#4794bc),to(#3a7999));background:-moz-linear-gradient(-90deg,#4794bc,#3a7999);border-bottom-color:#438bb1;}
button.classy.danger,a.button.classy.danger{color:#900;}
button.classy:hover,a.button.classy:hover{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);border-bottom-color:#0770a0;background:#0770a0;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#0ca6dd',endColorstr='#0770a0');background:-webkit-gradient(linear,0% 0,0% 100%,from(#0ca6dd),to(#0770a0));background:-moz-linear-gradient(-90deg,#0ca6dd,#0770a0);}
button.classy.mousedown,a.button.classy.mousedown{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);background:#0ca6dd;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#0ca6dd',endColorstr='#0770a0');background:-webkit-gradient(linear,0% 100%,0% 0,from(#0ca6dd),to(#0770a0));background:-moz-linear-gradient(90deg,#0ca6dd,#0770a0);}
button.classy.mousedown span,a.button.classy.mousedown span{background-position:0 -120px;}
button.classy::-moz-focus-inner{margin:-1px -3px;}
button.classy img,a.button.classy img{position:relative;top:-1px;margin-right:3px;vertical-align:middle;}
button.classy:disabled,.button.classy.disabled{opacity:.5;}
.minibutton{height:21px;padding:0 0 0 3px;font-size:11px;font-weight:bold;}
.minibutton,.minibutton.disabled:hover{position:relative;font-family:helvetica,arial,freesans,clean,sans-serif;display:inline-block;color:#333;text-shadow:1px 1px 0 #fff;white-space:nowrap;border:none;overflow:visible;cursor:pointer;border:1px solid #d4d4d4;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;background:#f4f4f4;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#f4f4f4),to(#ececec));background:-moz-linear-gradient(top,#f4f4f4,#ececec);}
button.minibutton{height:23px;}
.minibutton.lighter,.minibutton.disabled.lighter:hover{color:#333;text-shadow:1px 1px 0 #fff;border:none;background:#fafafa;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fafafa',endColorstr='#dddddd');background:-webkit-gradient(linear,left top,left bottom,from(#fafafa),to(#ddd));background:-moz-linear-gradient(top,#fafafa,#ddd);}
.minibutton.green,.minibutton.disabled.green:hover{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);background:#36b825;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#36b825',endColorstr='#28881b');background:-webkit-gradient(linear,left top,left bottom,from(#36b825),to(#28881b));background:-moz-linear-gradient(top,#36b825,#28881b);border-color:#4a993e;}
.minibutton.blue,.minibutton.disabled.blue:hover{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);background:#448da6;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#448da6',endColorstr='#32687b');background:-webkit-gradient(linear,left top,left bottom,from(#448da6),to(#32687b));background:-moz-linear-gradient(top,#448da6,#32687b);border-color:#275666;}
input[type=text]+.minibutton{margin-left:5px;}
button.minibutton::-moz-focus-inner{margin:-1px -3px;}
.minibutton.danger{color:#900;}
.minibutton.disabled.danger:hover{color:#900;border-color:#d4d4d4;background:#f4f4f4;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#f4f4f4),to(#ececec));background:-moz-linear-gradient(top,#f4f4f4,#ececec);}
.minibutton>span{display:block;height:21px;padding:0 9px 0 7px;line-height:21px;}
.minibutton:hover{color:#fff;text-decoration:none;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);border-color:#518cc6;border-bottom-color:#2a65a0;background:#599bdc;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#599bdc',endColorstr='#3072b3');background:-webkit-gradient(linear,left top,left bottom,from(#599bdc),to(#3072b3));background:-moz-linear-gradient(top,#599bdc,#3072b3);}
.minibutton.mousedown{border-color:#2a65a0;border-bottom-color:#518cc6;background:#3072b3;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#3072b3',endColorstr='#599bdc');background:-webkit-gradient(linear,left top,left bottom,from(#3072b3),to(#599bdc));background:-moz-linear-gradient(top,#3072b3,#599bdc);}
.minibutton.danger:hover{border-color:#c65651;border-bottom-color:#a0302a;background:#dc5f59;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#dc5f59',endColorstr='#b33630');background:-webkit-gradient(linear,left top,left bottom,from(#dc5f59),to(#b33630));background:-moz-linear-gradient(top,#dc5f59,#b33630);}
.minibutton.danger.mousedown{border-color:#a0302a;border-bottom-color:#c65651;background:#b33630;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#b33630',endColorstr='#dc5f59');background:-webkit-gradient(linear,left top,left bottom,from(#b33630),to(#dc5f59));background:-moz-linear-gradient(top,#b33630,#dc5f59);}
.minibutton.disabled,.minibutton.disabled:hover{opacity:.5;cursor:default;}
.minibutton.selected{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.5);border-color:#686868;background:#767676;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#767676',endColorstr='#9e9e9e');background:-webkit-gradient(linear,left top,left bottom,from(#767676),to(#9e9e9e));background:-moz-linear-gradient(top,#767676,#9e9e9e);}
.btn-admin .icon,.btn-watch .icon,.btn-download .icon,.btn-pull-request .icon,.btn-fork .icon,.btn-leave .icon,.btn-compare .icon,.btn-reply .icon,.btn-back .icon,.btn-forward .icon{position:relative;top:-1px;float:left;margin-left:-4px;width:18px;height:22px;background:url(/images/modules/buttons/minibutton_icons.png?v20100306) 0 0 no-repeat;}
.btn-forward .icon{float:right;margin-left:0;margin-right:-4px;}
.btn-admin .icon{width:16px;background-position:0 0;}
.btn-admin:hover .icon{background-position:0 -25px;}
.btn-watch .icon{background-position:-20px 0;}
.btn-watch:hover .icon{background-position:-20px -25px;}
.btn-download .icon{background-position:-40px 0;}
.btn-download:hover .icon{background-position:-40px -25px;}
.btn-pull-request .icon{width:17px;background-position:-60px 0;}
.btn-pull-request:hover .icon{background-position:-60px -25px;}
.btn-fork .icon{width:17px;background-position:-80px 0;}
.btn-fork:hover .icon{background-position:-80px -25px;}
.btn-leave .icon{width:15px;background-position:-120px 0;}
.btn-leave:hover .icon{background-position:-120px -25px;}
.btn-compare .icon{width:17px;background-position:-100px 0;}
.btn-compare:hover .icon{background-position:-100px -25px;}
.btn-reply .icon{width:16px;background-position:-140px 0;}
.btn-reply:hover .icon{background-position:-140px -25px;}
.btn-back .icon{width:16px;background-position:-160px 0;}
.btn-back:hover .icon{background-position:-160px -25px;}
.btn-forward .icon{width:16px;background-position:-180px 0;}
.btn-forward:hover .icon{background-position:-180px -25px;}
ul.big-actions{margin:15px 0 10px 0;float:right;}
ul.big-actions li{list-style-type:none;float:left;margin:0;}
.big-actions .minibutton,.minibutton.bigger{height:24px;padding:0 0 0 3px;font-size:12px;}
.big-actions .minibutton>span,.minibutton.bigger>span{height:24px;padding:0 10px 0 8px;line-height:24px;}
.featured-callout{margin:15px 0;padding:10px;font-size:12px;color:#333;background:#e8f0f5;border:1px solid #d2d9de;border-right-color:#e5e9ed;border-bottom-color:#e5e9ed;-webkit-border-radius:3px;-moz-border-radius:3px;}
.featured-callout .rule{width:100%;padding:0 10px;margin:10px 0 10px -10px;border-top:1px solid #c6d5df;border-bottom:1px solid #fff;}
.featured-callout h2{margin:0;font-size:14px;font-weight:bold;line-height:20px;color:#000;}
.featured-callout ol,.featured-callout ul{margin-left:20px;}
.featured-callout ol li,.featured-callout ul li{margin:5px 0;}
.featured-callout p:last-child{margin-bottom:0;}
.featured-callout p.more{font-weight:bold;}
.featured-callout pre.console{padding:5px;color:#eee;background:#333;border:1px solid #000;border-right-color:#222;border-bottom-color:#222;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.featured-callout pre.console code{font-size:11px;}
.featured-callout .diagram{margin:15px 0;text-align:center;}
.featured-callout .screenshot{margin:15px 0;padding:1px;background:#fff;border:1px solid #b4cad8;}
.mini-callout{margin:15px 0;padding:10px;color:#5d5900;border:1px solid #e7e7ce;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;background:#fffee8;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fffff6',endColorstr='#fffde3');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fffff6),to(#fffde3));background:-moz-linear-gradient(270deg,#fffff6,#fffde3);}
.mini-callout img{position:relative;top:-2px;vertical-align:middle;margin-right:5px;}
.inset-callout{margin:15px 0;padding:10px;font-size:12px;color:#333;background:#eee;border:1px solid #d5d5d5;border-right-color:#e5e5e5;border-bottom-color:#e5e5e5;-webkit-border-radius:3px;-moz-border-radius:3px;}
.help-callout{font-size:11px;}
.help-callout p:last-child{margin-bottom:0;}
.help-callout h2{margin-top:20px;}
.help-callout h2:first-child{margin:0;}
ul.features{margin:50px 0 20px 0;font-size:14px;font-weight:bold;color:#666;}
ul.features li{list-style-type:none;margin:5px 0;padding:2px 0 0 20px;background:url(/images/modules/featured_callout/big_check.png) 0 0 no-repeat;}
.featured-callout ul.features{margin:10px 0;font-size:12px;color:#2e3031;}
#planchange ul.features{margin-top:20px;}
.featured-callout h2.orgs-heading{padding-left:65px;background:url(/images/modules/featured_callout/orgs_icon.png) 0 50% no-repeat;}
.featured-callout h2.hooks-heading{padding-left:30px;background:url(/images/modules/featured_callout/hooks_icon.png) 0 50% no-repeat;}
.infotip{margin:15px 0;padding:10px;font-size:12px;color:#333;background:#fbffce;border:1px solid #deea53;border-right-color:#eff2c7;border-bottom-color:#eff2c7;-webkit-border-radius:3px;-moz-border-radius:3px;}
.infotip p{margin:0;}
.infotip p+p{margin-top:15px;}
.dashboard-notice{position:relative;margin:0 0 20px 0;padding:13px;font-size:12px;color:#333;border:1px solid #e7e7ce;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;background:#fffee8;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fffff6',endColorstr='#fffde3');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fffff6),to(#fffde3));background:-moz-linear-gradient(270deg,#fffff6,#fffde3);}
.dashboard-notice.winter{padding:0;border-color:#d1e5ff;background:#f5fbff;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f5fbff',endColorstr='#e4f0ff');background:-webkit-gradient(linear,left top,left bottom,from(#f5fbff),to(#e4f0ff));background:-moz-linear-gradient(top,#f5fbff,#e4f0ff);}
.dashboard-notice.winter .background{padding:13px;background:url(/images/modules/notices/winter-back.png) 0 0 no-repeat;}
.dashboard-notice .dismiss{position:absolute;display:block;top:5px;right:5px;width:18px;height:18px;text-indent:-9999px;background:url(/images/modules/notices/close.png) 0 0 no-repeat;cursor:pointer;}
.dashboard-notice .dismiss:hover{background-position:0 -50px;}
.dashboard-notice .title{margin-left:-13px;margin-bottom:13px;width:100%;padding:0 13px 13px;border-bottom:1px solid #e7e7ce;}
.dashboard-notice.winter .title{border-color:#d1e5ff;}
.dashboard-notice .title p{margin:0;font-size:14px;color:#666;}
.dashboard-notice h2{margin:0;font-size:16px;font-weight:normal;color:#000;}
.dashboard-notice p{margin-bottom:0;}
.dashboard-notice p.no-title{margin-top:0;padding-right:5px;}
.dashboard-notice .inset-figure{margin:0 0 15px 15px;float:right;padding:6px;background:#fff;border:1px solid #e4e4e4;border-right-color:#f4f4f4;border-bottom-color:#fff;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.dashboard-notice .inset-comment{margin:15px 0;padding:6px;background:#fff;color:#444;border:1px solid #e4e4e4;border-right-color:#f4f4f4;border-bottom-color:#fff;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.dashboard-notice ul{margin-left:25px;}
.dashboard-notice .coupon{margin:15px 0;padding:10px;text-align:center;font-weight:bold;font-size:20px;background:#fff;border:1px dashed #d1e5ff;}
.dashboard-notice.org-newbie .fancytitle{padding-left:60px;background:url(/images/modules/notices/orgs_title.png) 0 50% no-repeat;}
.octotip{position:relative;margin:10px 0;padding:5px 5px 5px 27px;color:#25494f;font-size:12px;background:url(/images/modules/callouts/octotip-octocat.png) 0 50% no-repeat #ccf1f9;border:1px solid #b1ecf8;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.frame .octotip{margin-top:0;}
.octotip p{margin:0;}
.octotip .dismiss{position:absolute;display:block;top:50%;right:5px;margin-top:-9px;width:18px;height:18px;text-indent:-9999px;background:url(/images/modules/notices/close.png) 0 0 no-repeat;cursor:pointer;}
.octotip .dismiss:hover{background-position:0 -50px;}
.kbd{display:inline-block;padding:3px 5px;color:#000;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:11px;background:#fefefe;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fefefe',endColorstr='#e7e7e7');background:-webkit-gradient(linear,left top,left bottom,from(#fefefe),to(#e7e7e7));background:-moz-linear-gradient(top,#fefefe,#e7e7e7);border:1px solid #cfcfcf;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
#facebox .badmono,.kbd.badmono{font-family:sans-serif;font-weight:bold;}
#code_search{margin-bottom:2em;}
#code_search .search{padding-top:.2em;height:7em;}
#code_search .search .site{width:650px;padding-top:1.15em;}
#code_search .search .site *{vertical-align:middle;}
#code_search .search .label{color:#777;font-size:110%;font-weight:bold;margin-bottom:.25em;}
#code_search .search .box span{font-size:130%;padding-top:.3em;}
#code_search .search .box input.text{height:1.4em;font-size:130%;padding-top:.3em;padding-left:.3em;border:2px solid #b4b4b4;}
#code_search .search .box select{font-size:120%;}
#code_search .search .box select option{padding-left:.5em;margin:.2em 0;}
#code_search_instructions{margin:2em 7em 0 7em;}
#code_search_instructions h2{background-color:#DDEAF3;padding:3px;}
#code_search_instructions p{color:#333;margin:10px 5px;}
#code_search_instructions table.instruction tr td{padding:3px;}
#code_search_instructions table.instruction tr td.inst{background:#eee;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;}
#code_search_results .header{border-top:1px solid #b8d1e3;background-color:#DDEAF3;padding:.3em .7em;overflow:hidden;margin-bottom:1.3em;}
#code_search_results .header .title{font-weight:bold;float:left;}
#code_search_results .header .info{float:right;color:#444;}
#code_search_results .results_and_sidebar{overflow:hidden;}
#code_search_results .results{float:left;width:52em;}
#code_search_results .result{margin-bottom:1.5em;}
#code_search_results .result .gravatar{line-height:0;float:left;margin-top:.2em;margin-right:.75em;padding:1px;border:1px solid #ccc;}
#code_search_results .result .title{font-size:110%;}
#code_search_results .result .title span.aka{font-weight:normal;}
#code_search_results .result .title span.language{color:#999;font-size:80%;font-weight:normal;position:relative;top:-.1em;}
#code_search_results .result .description{margin-bottom:.2em;}
#code_search_results .result .details{font-size:80%;color:#555;}
#code_search_results .result .details span{color:#aaa;padding:0 .25em;}
#code_search_results .more{margin-top:-.5em;margin-bottom:1em;}
#code_search_results .result .snippet{font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:75%;background-color:#f8f8ff;border:1px solid #dedede;padding:.5em;line-height:1.5em;color:#444;}
#code_search_results .result .snippet em{background-color:#FAFFA6;padding:.1em;}
#code_search_results .sidebar{float:right;width:15em;border-left:1px solid #DDEAF3;padding-left:1em;}
#code_search_results .sidebar h2{margin-bottom:0;}
#code_search_results .sidebar h3{margin-top:.5em;}
#code_search_results .sidebar ul{list-style-type:none;margin-bottom:1em;}
#code_search_results .sidebar ul li{color:#888;}
.comments-wrapper{margin:10px 0;padding:5px;background:#f2f2f2;-webkit-border-radius:5px;-moz-border-radius:5px;}
.comments-wrapper>.comment:first-child{margin-top:0;}
.comments-wrapper>.comment:last-child{margin-bottom:0;}
.new-comments .comment{margin:10px 0;border:1px solid #cacaca;}
.new-comments .comment.adminable:hover{border-color:#aaa;}
.new-comments .comment .cmeta{height:33px;padding:0 6px;border-bottom:1px solid #ccc;background:url(/images/modules/comments/metabar.gif) 0 0 repeat-x;}
.new-comments .commit-comment .cmeta,.new-comments .review-comment .cmeta,.new-comments .file-commit-comment .cmeta,.new-comments .gist-comment .cmeta,.new-comments .commit-list-comment .cmeta{background-position:0 -33px;}
.new-comments .repo-owner-tag .cmeta,.new-comments .gist-owner-tag .cmeta{background-position:0 -66px;}
.new-comments .comment .cmeta p.author{margin:0;float:left;font-size:12px;height:33px;line-height:33px;text-shadow:1px 1px 0 rgba(255,255,255,0.7);overflow:hidden;white-space:nowrap;text-overflow:ellipsis;}
.new-comments .comment .cmeta p.author a{color:#222;}
.new-comments .comment .cmeta p.author em a,.new-comments em.date a{color:#666;font-style:normal;}
.new-comments .comment .cmeta .gravatar{display:inline-block;margin-top:-2px;margin-right:3px;padding:1px;line-height:1px;vertical-align:middle;font-size:1px;background:#fff;border:1px solid #c8c8c8;}
.new-comments .comment .cmeta code{font-size:11px;}
.new-comments .comment .cmeta p.author em code a{color:#444;}
.new-comments .comment .cmeta p.info{float:right;margin:0;font-size:11px;height:33px;line-height:33px;}
.new-comments .comment .cmeta p.info em.date{display:inline;font-style:normal;color:#777;text-shadow:1px 1px 0 rgba(255,255,255,0.7);}
.new-comments .comment .cmeta p.info em.date,.comment .cmeta p.info em.date abbr{line-height:33px;}
.new-comments .comment .cmeta .icon{display:inline-block;margin-top:-2px;margin-left:5px;width:16px;height:16px;vertical-align:middle;background:url(/images/modules/comments/icons.png?v3) 0 0 no-repeat;}
.new-comments .comment .cmeta .author .icon{margin-left:0;}
.new-comments .commit-comment .cmeta .icon,.new-comments .gist-comment .cmeta .icon,.new-comments .review-comment .cmeta .icon,.new-comments .gist-comment .cmeta .icon{background-position:0 -100px;}
.new-comments .file-commit-comment .cmeta .icon{background-position:0 -200px;}
.new-comments .commit-list-comment .cmeta .icon{background-position:0 -300px;}
.new-comments .tag{position:relative;top:-1px;margin-left:5px;padding:1px 5px;font-size:11px;color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.2);background:#2d90c3;border:1px solid #26749c;border-right-color:#2d90c3;border-bottom-color:#2d90c3;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
.new-comments .repo-owner-tag .tag,.new-comments .gist-owner-tag .tag{background:#2cc03e;border-color:#259a33;border-right-color:#2cc03e;border-bottom-color:#2cc03e;}
.new-comments .comment .body{position:relative;padding:0 6px;color:#333;font-size:12px;overflow:auto;background:#fbfbfb;}
.new-comments .highlighted .comment .body{background:#fff;}
.new-comments .comment .body p{margin:10px 0;}
.new-comments .comment .content-body img{max-width:100%;}
.new-comments .comment .body .title{padding:5px 0;font-weight:bold;color:#000;border-bottom:1px solid #ddd;}
.new-comments .inset{padding:4px;background:#f1f1f1;border:1px solid #ccc;border-right-color:#e5e5e5;border-bottom-color:#e5e5e5;-webkit-border-radius:3px;-moz-border-radius:3px;}
.new-comments .commit-inset{background-color:#e3eaee;border-color:#b9c7d1;border-right-color:#dbe5eb;border-bottom-color:#dbe5eb;}
.new-comments .inset.highlighted{background-color:#ffd;border-color:#cfcfb4;border-right-color:#f1f1c7;border-bottom-color:#f1f1c7;}
.new-comments .inset .comment{margin:5px 0;}
.new-comments .inset .comment:first-child{margin-top:0;}
.new-comments .inset .comment:last-child{margin-bottom:0;}
.new-comments .inset h5{margin:0;font-size:10px;font-weight:normal;text-transform:uppercase;letter-spacing:1px;color:#666;text-shadow:1px 1px 0 rgba(255,255,255,0.7);}
.new-comments .commit-inset h5{color:#6c777f;}
.new-comments .commit-list-comment .body{padding:0;}
#compare .new-comments .commit-list-comment table.commits{border-width:0;margin-top:0;}
.new-comments .comment ul.actions{display:none;position:absolute;top:5px;right:5px;margin:0;}
.new-comments .adminable:hover ul.actions{display:block;}
.new-comments ul.actions li{list-style-type:none;margin:0 0 0 5px;float:left;}
.comment .form-content{margin:10px 0;}
.starting-comment .form-content{margin-top:0;}
.comment .form-content textarea{margin:0;width:100%;height:100px;}
.comment .form-content input[type=text]{margin-bottom:5px;width:99%;padding:4px 2px;}
.comment .form-content input.title-field{font-size:20px;font-weight:bold;}
.comment .form-content .form-actions{margin:10px 0 0 0;}
.comment p.error{font-weight:bold;color:#f00;}
.comment .error,.comment .context-loader{display:none;}
.comment .form-content{display:none;opacity:1.0;}
.comment.editing .formatted-content,.comment.editing .content-title,.comment.editing .infobar{display:none;}
.comment.editing .form-content{display:block;opacity:1.0;}
.comment.loading .context-loader{display:block;}
.comment.loading .formatted-content,.comment.loading .form-content{opacity:.5;}
.comment.error .error{display:block;}
.new-comments .closed-banner{margin:15px 0;height:7px;overflow:hidden;background:url(/images/modules/comments/closed_pattern.gif);-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.user-mention{font-weight:bold;color:#333;}
.message .user-mention{font-weight:normal;}
.email-format div{white-space:pre-wrap;}
.formatted-content .email-format{padding:1em 0!important;line-height:1.5em!important;}
.email-fragment,.email-quoted-reply{margin-bottom:10px;}
.email-quoted-reply,.email-signature-reply{color:#500050;}
.email-quoted-reply a{color:#500050;}
.email-hidden-reply{display:none;}
.email-hidden-toggle{display:block;font-size:75%;}
.line-comments{overflow:auto;padding:0;border-top:1px solid #ccc;border-bottom:1px solid #ddd;background:#fafafa!important;font-family:helvetica,arial,freesans,sans-serif!important;}
.line-comments .clipper{width:837px;padding:5px;}
tr:hover .line-comments{background:#fafafa!important;}
.line_numbers.comment-count{overflow:hidden;padding:0!important;background-image:url(/images/modules/comments/lines_back.gif);background-color:#f6f6f6!important;background-repeat:repeat-y;background-position:top left,top right;border:1px solid #ddd;border-left:none;border-right:none;vertical-align:top;text-align:center!important;}
.line_numbers.comment-count .counter{display:inline-block;padding:4px 8px 5px 24px;line-height:1.2;font-family:helvetica,arial,freesans,sans-serif!important;font-size:11px;font-weight:bold;color:#333!important;background:url(/images/modules/comments/icons.png) 5px -97px no-repeat #d6e3e8;border:1px solid #c0ccd0;border-top:none;-webkit-border-bottom-right-radius:3px;-webkit-border-bottom-left-radius:3px;-moz-border-radius-bottomright:3px;-moz-border-radius-bottomleft:3px;border-bottom-right-radius:3px;border-bottom-left-radius:3px;cursor:default!important;}
.line-comments .comment-form{margin:10px 0 5px 0;background-color:#eaeaea;}
.line-comments .comment-form textarea{font-size:12px;}
.line-comments .show-inline-comment-form{padding-top:5px;}
.line-comments .inline-comment-form .minibutton{margin-top:-11px;}
.line-comments .inline-comment-form .ajaxindicator{display:inline-block;margin-top:-5px;height:13px;}
.file-comments{padding:5px;font-family:helvetica,arial,freesans,sans-serif!important;background:#fafafa;border-top:1px solid #ddd;}
.comment-form-error,.issue-form-error{margin:-15px 0 15px 0;font-weight:bold;color:#a00;}
.comment-form{margin:-10px 0 10px 0;padding:5px;background:#eee;-webkit-border-radius:5px;-moz-border-radius:5px;}
.comment-form textarea{margin:0;width:100%;height:100px;}
.comment-form p.help{margin:3px 0 0 0;float:right;font-size:11px;color:#666;}
.comment-form ul.tabs{margin:0 0 5px 0;}
.comment-form ul.tabs li{list-style-type:none;margin:0;display:inline-block;}
.comment-form ul.tabs a{display:inline-block;padding:2px 8px;font-size:11px;font-weight:bold;text-decoration:none;color:#666;border:1px solid transparent;-webkit-border-radius:10px;-moz-border-radius:10px;}
.comment-form ul.tabs a.selected{color:#333;background:#fff;border-color:#bbb;border-right-color:#ddd;border-bottom-color:#ddd;}
.comment-form .comment{margin:5px 0 0 0;}
.page-commit-show h2{margin:20px 0 5px 0;font-size:16px;}
.page-commit-show h2 code{font-weight:normal;font-size:14px;}
.page-commit-show h2 em.quiet{font-style:normal;font-weight:normal;color:#888;}
.page-commit-show h2 .toggle{position:relative;top:5px;float:right;font-size:11px;font-weight:normal;color:#666;}
.page-commit-show h2 .toggle input{position:relative;top:1px;margin-right:5px;}
.page-commit-show #comments{margin-bottom:20px;}
.page-commit-show #gitnotes{background:#f5f5f5;padding:5px;}
.page-commit-show #gitnotes h2{margin:0;}
.page-commit-show #gitnotes-content{border:1px solid #aaa;background:#ffd;padding:10px;padding-top:15px;}
.page-commit-show #gitnotes-content h3{font-size:12px;background:#eea;padding:3px;}
.page-commit-show #gitnotes-content{border:1px solid #aaa;background:#ffd;padding:10px;}
.form-actions .tip{margin:0 0 10px 0;float:left;width:350px;padding:5px;text-align:left;font-size:12px;color:#333;background:#fafbd2;border:1px solid #e8eac0;border-right-color:#f5f7ce;border-bottom-color:#f5f7ce;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.form-actions .tip img{float:left;margin-right:10px;border:1px solid #ccc;}
.form-actions .tip p{margin:2px 0;}
.only-commit-comments .inline-comment{display:none;}
.inline-comment-placeholder{height:30px;background:url(/images/modules/ajax/indicator.gif) 50% 50% no-repeat;}
.inline-comments .action-text{display:none;}
*{margin:0;padding:0;}
html,body{height:100%;color:black;}
body{background-color:white;font:13.34px helvetica,arial,freesans,clean,sans-serif;*font-size:small;}
#main{background:#fff url(/images/modules/header/background-v2.png) 0 0 repeat-x;}
table{font-size:inherit;font:100%;}
input[type=text],input[type=password],input[type=image],textarea{font:99% helvetica,arial,freesans,sans-serif;}
select,option{padding:0 .25em;}
optgroup{margin-top:.5em;}
input.text{padding:1px 0;}
pre,code{font:12px Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;}
body *{line-height:1.4em;}
p{margin:1em 0;}
img{border:0;}
abbr{border-bottom:none;}
.clearfix:after{content:".";display:block;height:0;clear:both;visibility:hidden;}
* html .clearfix{height:1%;}
.clearfix{display:inline-block;}
.clearfix{display:block;}
html{overflow-y:scroll;}
a{color:#4183c4;text-decoration:none;}
a:hover{text-decoration:underline;}
.usingMouse a{outline:none;}
a.danger{color:#c00;}
a.action{color:#d00;text-decoration:underline;}
.sparkline{display:none;}
.right{float:right;}
.left{float:left;}
.hidden{display:none;}
img.help{vertical-align:middle;}
.notification{background:#FFFBE2 none repeat scroll 0;border:1px solid #FFE222;padding:1em;margin:1em 0;font-weight:bold;}
.warning{background:#fffccc;font-weight:bold;padding:.5em;margin-bottom:.8em;}
.error_box{background:#FFEBE8 none repeat scroll 0;border:1px solid #DD3C10;padding:1em;font-weight:bold;}
.rule{clear:both;margin:15px 0;height:0;overflow:hidden;border-bottom:1px solid #ddd;}
.corner{-moz-border-radius:8px;-webkit-border-radius:8px;border-radius:8px;padding:3px;}
#spinner{height:16px;width:16px;background:transparent;border:none;margin-right:0;}
.clear{clear:both;}
.columns:after{content:".";display:block;height:0;clear:both;visibility:hidden;}
* html .columns{height:1%;}
.columns{display:inline-block;}
.columns{display:block;}
#facebox .content{width:425px;color:#333;font-size:12px;background:-webkit-gradient(linear,0% 0,5% 100%,from(#f4f9fb),to(#fff));background:-moz-linear-gradient(100% 100% 107deg,#fff,#f4f9fb);}
#facebox .content.wider{width:500px;}
#facebox pre{padding:5px 10px;border:1px solid #ddd;border-bottom-color:#eee;border-right-color:#eee;background:#eee;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
#facebox pre.console{color:#fff;background:#333;border-color:#000;border-right-color:#333;border-bottom-color:#333;}
#facebox ul,#facebox ol{margin:15px 0 15px 20px;}
#facebox ul li{margin:5px 0;}
#facebox h2{width:100%;margin:0 0 10px -10px;padding:0 10px 10px 10px;font-size:16px;border-bottom:1px solid #ddd!important;}
#facebox h3{margin-bottom:-0.5em;font-size:14px;color:#000;}
#facebox .rule{width:100%;padding:0 10px;margin-left:-10px;}
#facebox input[type=text]{width:96%;padding:5px 5px;font-size:12px;}
#facebox .form-actions{margin-top:10px;}
#facebox .warning{width:100%;padding:5px 10px;margin-top:-9px;margin-left:-10px;font-weight:bold;color:#900;background:url(/images/icons/bigwarning.png) 10px 50% no-repeat #fffbc9;border-bottom:1px solid #ede7a3;}
#facebox .warning p{margin-left:45px;}
#facebox .full-button{margin-top:10px;}
#facebox .full-button .classy{margin:0;display:block;width:100%;}
#facebox .full-button .classy span{display:block;text-align:center;}
#compare h2{font-size:20px;margin:15px 0 15px 0;}
#compare p.subtext{margin:-15px 0 10px 0;color:#666;}
#compare h2 .tag{position:relative;top:-3px;display:inline-block;padding:3px 8px;font-size:12px;color:#666;background:#eee;-webkit-border-radius:3px;-moz-border-radius:3px;}
.commit-ref{padding:2px 5px;line-height:19px;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:12px;font-weight:normal;color:#fff;text-shadow:-1px -1px 0 #000;text-decoration:none;background:url(/images/modules/compare/sha_gradient.gif) 0 0 repeat-x #333;-webkit-border-radius:3px;-moz-border-radius:3px;}
.commit-ref .user{font-weight:normal;color:#ccc;}
a.commit-ref:hover{text-shadow:-1px -1px 0 #04284b;background-position:0 -19px;text-decoration:none;}
.compare-range{margin-top:-15px;float:right;}
.compare-range em{padding:0 4px;font-style:normal;color:#666;}
.compare-range .switch{display:inline-block;width:16px;height:16px;text-indent:-9999px;background:url(/images/modules/compare/switch_icon.png?v2) 0 0 no-repeat;}
.compare-range .minibutton{margin-right:15px;}
#compare .compare-cutoff{margin-top:15px;margin-bottom:-15px;height:35px;line-height:37px;font-size:12px;font-weight:bold;color:#000;text-align:center;background:url(/images/modules/compare/compare_too_big.gif) 0 0 no-repeat;}
.commits-condensed{margin-top:15px;border:1px solid #ddd;border-width:1px 1px 0 1px;}
.commits-condensed td{padding:.4em .5em .4em 1.5em;padding-left:1.5em;vertical-align:middle;border-bottom:1px solid #ddd;}
.commits-condensed tr:nth-child(2n) td{background:#f5f5f5;}
.commits-condensed td.commit{padding-left:.5em;}
.commits-condensed span.gravatar{display:block;width:20px;height:20px;line-height:1px;padding:1px;border:1px solid #ddd;background:#fff;}
.commits-condensed td.author{padding-left:0;}
.commits-condensed td.author a{color:#333;}
.commits-condensed td.date{text-align:right;color:#777;}
.commits-condensed td.message a{color:#333;}
.commits-condensed code{font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:12px;}
.commits-condensed tr.merge td{padding-top:.2em;padding-bottom:.2em;background:#eee;}
.commits-condensed tr.merge td.gravatar span{height:16px;width:16px;}
.commits-condensed tr.merge td.commit a{font-size:10px;color:#6c8286;}
.commits-condensed tr.merge td.author{font-size:10px;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;color:#666;}
.commits-condensed tr.merge td.author a{color:#666;}
.commits-condensed tr.merge td.date{font-size:10px;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;}
.commits-condensed tr.merge td.message a{font-size:10px;color:#666;}
.commit-preview{margin:10px 0 0 0;font-size:11px;}
.commit-preview>p{margin:16px 0;font-size:14px;text-align:center;}
.commit-preview p.name{margin:0;height:20px;line-height:20px;font-size:12px;color:#5b6375;}
.commit-preview p.name .avatar{float:left;margin-right:5px;width:16px;height:16px;padding:1px;background:#fff;border:1px solid #cedadf;}
.commit-preview p.name a{font-weight:bold;color:#000;}
.commit-preview p.name .date{color:#5b6375;}
.commit-preview .message,.commit-preview p.error{clear:both;padding:5px;background:#eaf2f5;border:1px solid #bedce7;}
.commit-preview .message pre{font-size:11px;color:#333;white-space:pre-wrap;word-wrap:break-word;}
.commit-preview p.error{text-align:center;font-size:12px;font-weight:bold;color:#000;}
.commit-preview .message p.commit-id{margin:5px 0 0 0;padding:0;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:11px;}
div.edu_contact_hidden{display:none;margin:1em 0;}
div.edu_contact_hidden p:first-child{margin-top:0;}
a.button{height:23px;padding:0 10px;line-height:23px;font-size:11px;font-weight:bold;color:#fff;text-shadow:-1px -1px 0 #333;-webkit-border-radius:3px;-moz-border-radius:3px;background:url(/images/modules/buttons/black.gif) 0 0 repeat-x;}
a.button{-webkit-text-stroke:1px transparent;}
@media only screen and(max-device-width:480px){a.button{-webkit-text-stroke:0 black;}
}
a.button:hover{background-position:0 -23px;text-decoration:none;}
.bootcamp{margin:0 0 20px 0;}
.bootcamp h1{color:#fff;font-size:16px;font-weight:bold;background-color:#405a6a;background:-moz-linear-gradient(center top,'#829AA8','#405A6A');filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#829aa8',endColorstr='#405a6a');background:-webkit-gradient(linear,left top,left bottom,from(#829aa8),to(#405a6a));background:-moz-linear-gradient(top,#829aa8,#405a6a);border:1px solid #677c89;border-bottom-color:#6b808d;border-radius:5px 5px 0 0;-moz-border-radius:5px 5px 0 0;-webkit-border-radius:5px 5px 0 0;text-shadow:0 -1px 0 rgba(0,0,0,0.7);margin:0;padding:8px 18px;position:relative;}
.bootcamp h1 a{color:#fff;text-decoration:none;}
.bootcamp h1 span{color:#e9f1f4;font-size:70%;font-weight:normal;text-shadow:none;}
.bootcamp .js-dismiss-bootcamp{display:block;width:19px;height:19px;background-image:url(/images/modules/dashboard/bootcamp/close_sprite.png);background-repeat:no-repeat;background-position:0 0;position:absolute;right:5px;top:50%;margin-top:-10px;}
.bootcamp .js-dismiss-bootcamp:hover{background-position:0 -19px;}
.bootcamp .bootcamp-body{padding:10px 0 10px 10px;background-color:#e9f1f4;overflow:hidden;border-style:solid;border-width:1px 1px 2px;border-color:#e9f1f4 #d8dee2 #d8dee2;border-radius:0 0 5px 5px;-moz-border-radius:0 0 5px 5px;-webkit-border-radius:0 0 5px 5px;}
.bootcampo ul{list-style-type:none;position:relative;}
.bootcamp ul li{color:#666;font-size:13px;font-weight:normal;background-color:#fffff5;background:-moz-linear-gradient(center top,'#fffff5','#f5f3b4');filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fffff5',endColorstr='#f5f3b4');background:-webkit-gradient(linear,left top,left bottom,from(#fffff5),to(#f5f3b4));background:-moz-linear-gradient(top,#fffff5,#f5f3b4);border:1px solid #dfddb5;border-radius:5px 5px 5px 5px;-moz-border-radius:5px 5px 5px 5px;-webkit-border-radius:5px 5px 5px 5px;display:block;width:215px;height:215px;float:left;position:relative;margin:0 10px 0 0;-moz-box-shadow:0 1px 0 #fff;-webkit-box-shadow:0 1px 0 #fff;box-shadow:0 1px 0 #fff;}
.bootcamp ul li:hover{background:-moz-linear-gradient(center top,'#fcfce9','#f1eea3');filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fcfce9',endColorstr='#f1eea3');background:-webkit-gradient(linear,left top,left bottom,from(#fcfce9),to(#f1eea3));background:-moz-linear-gradient(top,#fcfce9,#f1eea3);border:1px solid #d6d4ad;}
.bootcamp ul li a{color:#666;text-decoration:none;}
.bootcamp .image{display:block;position:relative;height:133px;border-bottom:1px solid #f1efaf;background-repeat:no-repeat;background-position:center center;}
.bootcamp .setup .image{background-image:url(/images/modules/dashboard/bootcamp/octocat_setup.png);}
.bootcamp .create-a-repo .image{background-image:url(/images/modules/dashboard/bootcamp/octocat_create.png);}
.bootcamp .fork-a-repo .image{background-image:url(/images/modules/dashboard/bootcamp/octocat_fork.png);}
.bootcamp .be-social .image{background-image:url(/images/modules/dashboard/bootcamp/octocat_social.png);}
.bootcamp ul li:hover .image{border-bottom:1px solid #f1eea3;}
.bootcamp .desc{padding:13px 0 15px 15px;display:block;height:50px;overflow:hidden;border-top:1px solid #fff;background-repeat:no-repeat;position:relative;z-index:2;}
.bootcamp ul li:hover .desc{border-top:1px solid #fcfce9;}
.bootcamp .desc h2{margin:0;padding:0;font-size:15px;color:#393939;}
.bootcamp .desc p{margin:0;padding:0;line-height:1.2em;}
.bootcamp .step-number{background-image:url(/images/modules/dashboard/bootcamp/largenumb_sprites.png);background-repeat:no-repeat;display:block;width:64px;height:80px;position:absolute;right:0;bottom:0;z-index:0;}
.bootcamp .one{background-position:0 0;}
.bootcamp ul li:hover .one{background-position:0 -80px;}
.bootcamp .two{background-position:-64px 0;}
.bootcamp ul li:hover .two{background-position:-64px -80px;}
.bootcamp .three{background-position:-128px 0;}
.bootcamp ul li:hover .three{background-position:-128px -80px;}
.bootcamp .four{background-position:-192px 0;}
.bootcamp ul li:hover .four{background-position:-192px -80px;}
#dashboard .repos{margin:15px 0;width:333px;padding:0 2px;background:url(/images/modules/repo_list/box_back.gif) 0 0 repeat-y;}
#dashboard .repos .bottom-bar{width:100%;min-height:13px;padding:0 2px 3px 2px;margin-left:-2px;background:url(/images/modules/repo_list/box_bottom.gif) 0 100% no-repeat;}
#dashboard .repos a.show-more{display:block;padding:10px;font-size:14px;font-weight:bold;color:#999;}
#dashboard .repos .bottom-bar img{margin:10px;}
#dashboard .repos .top-bar{position:relative;margin:0 0 0 -2px;width:100%;height:44px;padding:0 2px;background:url(/images/modules/repo_list/box_top.gif) 0 0 no-repeat;}
#dashboard .repos h2{margin:0;height:44px;line-height:44px;padding:0 10px;font-size:16px;color:#52595d;}
#dashboard .repos h2 em{color:#99a4aa;font-style:normal;}
#dashboard .repos a.button{position:absolute;top:11px;right:10px;}
#dashboard .filter-bar{padding:10px 10px 0 10px;background:#fafafb;border-bottom:1px solid #e1e1e2;}
#dashboard .filter-bar .filter_input{width:289px;padding:2px 12px;height:15px;background:url(/images/modules/repo_list/filter_input.gif) 0 -19px no-repeat;border:none;}
#dashboard .filter-bar .filter_input.native{width:100%;height:auto;padding:2px 5px;font-size:11px;background-image:none;}
#dashboard .filter-bar .filter_input.placeholder{background-position:0 0;}
#dashboard .filter-bar .filter_input:focus{background-position:0 -19px;}
#dashboard .filter-bar ul.repo_filterer{margin:5px 0 0 0;text-align:right;}
#dashboard .filter-bar li{display:inline;margin:0 0 0 10px;padding:0;font-size:11px;}
#dashboard .filter-bar li.all_repos{position:relative;top:2px;float:left;margin:0;}
#dashboard .filter-bar li a{display:inline-block;padding-bottom:8px;color:#777;}
#dashboard .filter-bar li a.filter_selected{color:#000;font-weight:bold;background:url(/images/modules/repo_list/filter_selected_bit.gif) 50% 100% no-repeat;}
#dashboard ul.repo_list{margin:0;}
#dashboard ul.repo_list li{display:block;margin:0;padding:0;}
#dashboard ul.repo_list .public{border:none;border-bottom:1px solid #e5e5e5;background:url(/images/icons/public.png) 10px 8px no-repeat #fff;}
#dashboard ul.repo_list .private{border:none;border-bottom:1px solid #e5e5e5;background:url(/images/icons/private.png) 10px 8px no-repeat #fffeeb;}
#dashboard ul.repo_list li a{display:block;padding:6px 10px 5px 32px;font-size:14px;background:url(/images/modules/repo_list/arrow-40.png) 97% 50% no-repeat;}
#dashboard ul.repo_list li.private a{background-image:url(/images/modules/repo_list/arrow-60.png);}
#dashboard ul.repo_list li a:hover{background-image:url(/images/modules/repo_list/arrow-80.png);}
#dashboard ul.repo_list li.private a:hover{background-image:url(/images/modules/repo_list/arrow-90.png);}
#dashboard ul.repo_list li a .repo{font-weight:bold;}
#dashboard p.notice{margin:15px 10px 0 10px;font-weight:bold;font-size:12px;text-align:center;}
.octofication{margin:15px 0;}
#dashboard .octofication{float:right;width:337px;}
.octofication .message{padding:10px 10px 10px 35px;background:url(/images/modules/dashboard/octofication.png) 0 50% no-repeat #dcf7dd;border:1px solid #bbd2bc;border-top-color:#d1ead2;-webkit-border-radius:5px;-moz-border-radius:5px;}
.octofication .message h3{margin:0;font-size:14px;text-shadow:1px 1px 0 #fff;}
.octofication .message p{font-size:12px;color:#333;padding:0;margin:0;}
.octofication .message p+p{margin-top:15px;}
.octofication ul.actions{margin:5px 0 0 0;font-size:10px;height:15px;}
.octofication ul.actions li{list-style-type:none;margin:0;}
.octofication li.hide{float:left;font-weight:bold;}
.octofication li.hide a{color:#666;text-decoration:none;}
.octofication li.hide a:hover{color:#000;}
.octofication li.hide a:hover strong{color:#a60000;}
.octofication li.more{float:right;}
#dashboard .github-jobs-promotion{float:right;width:337px;}
.github-jobs-promotion p{position:relative;padding:10px 18px;font-size:12px;text-align:center;color:#1b3650;border:1px solid #cee0e7;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;background:#e4f0ff;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f5fbff',endColorstr='#e4f0ff');background:-webkit-gradient(linear,left top,left bottom,from(#f5fbff),to(#e4f0ff));background:-moz-linear-gradient(top,#f5fbff,#e4f0ff);}
.github-jobs-promotion p a{color:#1b3650;}
.github-jobs-promotion a.jobs-logo{display:block;text-align:center;font-size:11px;color:#999;}
.github-jobs-promotion a.jobs-logo strong{display:inline-block;width:62px;height:15px;text-indent:-9999px;background:url(/images/modules/jobs/logo.png) 0 0 no-repeat;}
.github-jobs-promotion .job-location{white-space:nowrap;}
.github-jobs-promotion .info{position:absolute;bottom:4px;right:4px;display:block;width:13px;height:13px;text-decoration:none;text-indent:-9999px;opacity:.5;cursor:pointer;background:url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAZ1JREFUeNp0kt0rREEYxt95Z87XHlxpo22VuJCPXG57IUVbpJQL5ZJ75U/wXyhKyrWSCyQXQigS2965cIEt2RLZXWvtmfG+p85a4qlznjkz85tn3jMjjDEQafc426QDnaHmCD22EOJRoNgeHxo8hwaJCNo5vJ4iW5JKtkmpgADgMR0EoI3ep765TLo3X4d2jrKziGLNcVywbReklOB7FhTfPwgyUK1WoFar5RExNZrqyePeSa5bSlz2Yj54ng/KsiARb4GBrji0+F747Xoe2I6ToJB1TlKUtGDbnk0CpARW4aUceqlSC7eJqGgHAEbrkYOLm7RCgRMWrcYDLN9V0NfZGrbLlU94LVXroFI2bbOaIQY7OIEHotXvn97gt0KQ5yEmqDZ8jYBInPCXhDAMF5HeZ41nxYq5Vt2V/F7QGEoT8hIl4iqfRQRyTcl4c9hmdyzZAJm8VLgZntPR1e0WFTmplIL/pLUmKJhO9yc3kDuktGbod64Ewed/wDMRMwz8uEas09zDGNk8CjFM3kT13pFvU/GLqd72QjTvS4ABABRRlkohJ02VAAAAAElFTkSuQmCC);}
.github-jobs-promotion p:hover .info{opacity:1.0;}
#dashboard .codeconf-promotion{float:right;margin:15px 0 0 0;width:337px;}
.codeconf-promotion{border:1px solid #000;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;background:#454545;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#454545',endColorstr='#000000');background:-webkit-gradient(linear,left top,left bottom,from(#454545),to(#000));background:-moz-linear-gradient(top,#454545,#000);}
.codeconf-promotion p{position:relative;margin:0;padding:7px 18px 7px 60px;font-size:12px;text-align:left;color:#fff;background:url(/images/modules/dashboard/codeconf-promo.png) -5px 50% no-repeat;}
.codeconf-promotion strong{display:block;color:#fff;}
.codeconf-promotion a{display:block;color:#ccc;text-decoration:none;}
.page-downloads h3{margin:15px 0 5px 0;font-size:14px;}
.page-downloads .manage-button{float:right;margin-top:-28px;}
.page-downloads p.bigmessage{margin:30px 0;text-align:center;font-size:16px;color:#333;}
.qrcode{text-align:center;}
.uploader{position:relative;margin:10px 0 20px 0;padding-bottom:1px;}
.page-downloads .uploader h3{font-size:16px;margin:0 0 0 -10px;}
table.uploads{width:918px;margin-left:-9px;border-spacing:0;border-collapse:collapse;}
table.uploads td{padding:10px 0 15px;vertical-align:bottom;}
table.uploads td.choose{width:1%;padding-left:9px;padding-right:15px;}
table.uploads td.action{width:1%;padding-left:20px;padding-right:9px;}
table.uploads .description dl.form{margin:0;}
table.uploads .description dl.form dt{margin-top:0;font-size:11px;}
.uploading .description dl.form dt,.fallback-disabled .description dl.form dt{color:#888;}
table.uploads .error .description dl.form dt{color:#c00;}
table.uploads .succeeded .description dl.form dt{color:#007a09;}
table.uploads .description input[type=text]{width:100%;}
table.uploads tr{border-top:1px solid #ddd;}
table.uploads tr:first-child{border-top:none;}
.choose .upload-button-wrapper{position:relative;}
.choose .file-minibutton{display:block;padding:5px;font-size:11px;font-weight:bold;color:#333;text-align:center;text-shadow:1px 1px 0 #fff;white-space:nowrap;border:none;overflow:visible;cursor:pointer;border:1px solid #d4d4d4;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;background:#fff;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#ffffff',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#fff),to(#ececec));background:-moz-linear-gradient(top,#fff,#ececec);}
.choose .upload-button-wrapper:hover .file-minibutton{color:#fff;text-decoration:none;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);border-color:#518cc6;border-bottom-color:#2a65a0;background:#599bdc;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#599bdc',endColorstr='#3072b3');background:-webkit-gradient(linear,left top,left bottom,from(#599bdc),to(#3072b3));background:-moz-linear-gradient(top,#599bdc,#3072b3);}
.choose .file-minibutton .icon{display:block;width:18px;height:22px;margin:0 auto;background:url(/images/icons/choose-file.png) 0 0 no-repeat;}
.choose .upload-button-wrapper:hover .file-minibutton .icon{background-position:0 -100px;}
.choose .swfupload{position:absolute;top:0;left:-1px;width:100%;height:100%;}
.upload-button-wrapper .html-file-field{position:absolute;top:0;left:0;width:100%;height:100%;opacity:.01;filter:alpha(opacity=1);}
.swfupload-ready .upload-button-wrapper .html-file-field{display:none;}
.file-to-upload{display:none;padding:7px 10px;text-shadow:1px 1px 0 rgba(255,255,255,1);white-space:nowrap;background:#fff;border:1px solid #ddd;border-bottom-color:#fff;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.uploading .file-to-upload{background:url(/images/modules/download/diagonal_lines.gif) 0 0;}
.error .file-to-upload{border:1px solid #a00;background:#c00;}
.file-to-upload p{margin:0;padding-left:25px;background:url(/images/modules/download/check.png) 0 50% no-repeat;}
.error .file-to-upload p{background-image:url(/images/modules/download/error.png);}
.succeeded .file-to-upload p{background-image:url(/images/modules/download/check-green.png);}
.file-to-upload strong{display:block;color:#000;font-weight:normal;}
.file-to-upload em{display:block;color:#888;font-style:normal;font-size:11px;}
.error .file-to-upload strong,.error .file-to-upload em{color:#fff;text-shadow:none;}
.filechosen .choose .file-to-upload{display:block;}
.filechosen .choose .upload-button-wrapper{display:none;}
.uploader .usagebars{position:absolute;top:0;right:10px;}
.uploader .usagebars dl{padding:0;border:none;}
.uploader .usagebars dt.numbers{display:none;}
.uploader .usagebars dt.label{height:24px;padding-right:10px;line-height:24px;color:#666;}
.uploader .usagebars dd.bar{float:left;clear:none;width:200px;}
ol.download-list{margin:5px 0 35px 0;border-top:1px solid #ddd;}
ol.download-list li{list-style-type:none;margin:0;padding:7px 5px 7px 26px;border-bottom:1px solid #ddd;background:url(/images/icons/download-unknown.png) 5px 7px no-repeat;}
ol.download-list li:nth-child(2n){background-color:#f6f6f6;}
ol.download-list li.ctype-zip{background-image:url(/images/icons/download-zip.png);}
ol.download-list li.ctype-media{background-image:url(/images/icons/download-media.png);}
ol.download-list li.ctype-text{background-image:url(/images/icons/download-text.png);}
ol.download-list li.ctype-android{background-image:url(/images/icons/qrcode.png);}
ol.download-list li.ctype-pdf{background-image:url(/images/icons/download-pdf.png);}
ol.download-list li.ctype-tag{background-image:url(/images/icons/tag.png);}
.download-list .download-stats{float:right;margin-top:8px;font-size:12px;color:#666;}
.download-list .download-stats strong{color:#333;}
.download-list .delete-button{display:none;float:right;margin-top:8px;}
.managing .download-stats{display:none;}
.managing .delete-button{display:block;}
.download-list h4{margin:0;font-size:12px;font-weight:normal;color:#333;}
.download-list h4 a{font-weight:bold;}
.download-list h4 .alt-download-links{opacity:0;filter:alpha(opacity=0);padding-left:5px;-webkit-transition:opacity .1s linear;}
.download-list li:hover h4 .alt-download-links{opacity:1;filter:alpha(opacity=100);}
.download-list h4 .alt-download-links a{font-size:10px;padding-left:10px;padding-right:2px;background:url(/images/modules/download/mini_down_arrow.png) 0 50% no-repeat;}
.download-list p{margin:1px 0 0 0;font-size:11px;color:#999;}
.download-list p a{color:#999;}
#editbar{border-left:1px solid #888;border-top:1px solid #888;border-right:1px solid #888;width:100%;overflow:hidden;font-family:sans-serif;font-size:13px;}
#editbar .inner{width:100%;padding:0;margin:0;border:none;}
#editbar .current{display:block!important;}
#editbar .menu{overflow:hidden;background:#fff;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#ffffff',endColorstr='#ebf1ff');background:-webkit-gradient(linear,left top,left bottom,from(#fff),to(#ebf1ff));background:-moz-linear-gradient(top,#fff,#ebf1ff);}
#editbar .group{float:left;height:26px;margin:3px;padding-right:6px;}
#editbar .group-right{float:right;}
#editbar .group-separator{border-right:1px solid #ddd;}
#editbar .button{width:22px;height:22px;background:#e7ecfb url(/images/modules/wiki/editbar-buttons.png);border:1px solid #ddd;text-indent:-100px;cursor:pointer;overflow:hidden;padding:1px;display:block;float:left;margin:0 2px;-moz-border-radius:2px;-webkit-border-radius:2px;-khtml-border-radius:2px;border-radius:2px;background-repeat:no-repeat;}
#editbar .button:hover{background-color:#d9dde7;border-color:#aaa;}
#editbar .bold{background-position:-97px 4px;}
#editbar .italic{background-position:-147px 4px;}
#editbar .link{background-position:-197px 4px;}
#editbar .image{background-position:-247px 4px;}
#editbar .ul{background-position:3px 4px;}
#editbar .ol{background-position:-47px 4px;}
#editbar .tab{float:left;display:block;}
#editbar .tab a{cursor:pointer;display:inline-block;float:left;height:26px;padding-left:18px;padding-right:12px;line-height:26px;text-decoration:none;background-image:url(/images/modules/wiki/twiddle-right.png);background-position:0 50%;background-repeat:no-repeat;color:blue;}
#editbar .tab a.open{background-image:url(/images/modules/wiki/twiddle-down.png);color:#333;}
#editbar .tab a.open:hover{text-decoration:none;}
#editbar .tab a:hover{text-decoration:underline;}
#editbar .sections{clear:both;float:left;width:100%;overflow:visible;border-top:1px solid #888;height:185px;background-color:#E0EEF7;display:none;}
#editbar .sections .toc{float:left;width:20%;overflow:auto;}
#editbar .sections .toc div{cursor:pointer;padding:4px 4px 4px 6px;background-color:#E0EEF7;color:blue;}
#editbar .sections .toc div.current{cursor:default;background-color:white;color:#333;}
#editbar .sections .pages{overflow:auto;background-color:white;float:right;width:80%;height:185px;}
#editbar .sections .page{display:none;}
#editbar .sections .pages th{color:#999;font-weight:bold;padding:5px;text-align:left;}
#editbar .sections .pages td{color:black;padding:5px;border-top:1px solid #eee;}
#editbar .sections .pages span.invisible{color:#bbb;padding-left:1px;}
#editbar .sections .pages .shortcodes th{text-align:center;}
#editbar .sections .pages .shortcodes ul{list-style-type:none;}
.explorecols .main{float:left;width:500px;}
.explorecols .sidebar{float:right;width:390px;}
.explore h2{margin-top:15px;margin-bottom:0;padding-bottom:5px;font-size:16px;color:#333;border-bottom:1px solid #ddd!important;}
.ranked-repositories+h2{margin-top:30px;}
.explore p{margin:.75em 0;}
.explore .trending-repositories{margin-bottom:20px;position:relative;}
.explore h2.trending-heading{padding-left:22px;background:url(/images/modules/explore/trending_icon.png) 0 3px no-repeat;}
.explore h2.trending-heading .updated{font-size:12px;color:#aaa;float:right;}
.explore h2.trending-heading .times{font-size:12px;font-weight:normal;color:#000;float:right;}
.explore h2.trending-heading .times a{color:#4183C4;font-weight:bold;}
.explore h2.featured-heading{padding-left:22px;background:url(/images/modules/explore/featured_icon.png) 0 3px no-repeat;}
.explore h2 .feed{float:right;padding-left:24px;height:14px;line-height:14px;font-size:12px;background:url(/images/icons/feed.png) 5px 50% no-repeat #fff;}
.ranked-repositories{margin:0 0 10px 0;}
.ranked-repositories>li{position:relative;list-style-type:none;margin:0;padding:5px 0;min-height:30px;border-bottom:1px solid #ddd;}
.ranked-repositories>li.last{border-bottom:none;}
.ranked-repositories h3{margin:0;width:410px;font-size:14px;color:#999;}
.ranked-repositories h3.yours{background:url(/images/modules/explore/gold_star.png) 0 3px no-repeat;}
.ranked-repositories h3.yours .goldstar{display:inline-block;width:11px;height:12px;}
.ranked-repositories p{margin:0;width:410px;font-size:12px;color:#333;}
.ranked-repositories ul.repo-stats{position:absolute;top:8px;right:0;font-size:11px;font-weight:bold;}
.ranked-repositories .meta{margin-top:3px;font-size:11px;}
.ranked-repositories .meta a{padding:2px 5px;color:#666;background:#eee;-webkit-border-radius:2px;-moz-border-radius:2px;}
.podcast-player .title{margin-top:0;}
.podcast-player .title span{font-weight:normal;font-size:13px;color:#999;}
.podcast-player .artist{display:none;}
.podcast-player h3{font-size:14px;color:#000;}
.podcast-player p{margin:0;margin-top:5px;}
.podcast-player p.download{margin:5px 0;margin-top:5px;float:left;font-size:11px;}
.podcast-player p.date{margin:5px 0;float:right;font-size:11px;}
.podcast-player p.date strong{display:none;}
.podcast-player p.description{clear:both;padding-top:5px;border-top:1px solid #d2d9de;}
.podcast-player p.description strong{display:none;}
.podcasts{margin:20px 0 0 0;}
.podcasts li{list-style-type:none;margin:10px;padding-left:22px;font-size:12px;background:url(/images/modules/explore/podcast_icon.png) 0 0 no-repeat;}
.podcasts li em.date{margin-top:-2px;display:block;font-size:11px;color:#666;font-style:normal;}
div.baconplayer{height:40px;}
.baconplayer .inner-player{background:#343434;padding:0 0 10px;margin:20px -10px 0;height:25px;}
.baconplayer a{text-decoration:none;}
.baconplayer .dingus{float:left;margin:-8px 0 0 8px;width:52px;height:52px;text-indent:-9999px;cursor:pointer;}
.baconplayer .play{background:url(/images/modules/explore/play_button.png) 0 0 no-repeat;}
.baconplayer .pause{display:none;background:url(/images/modules/explore/pause_button.png) 0 0 no-repeat;}
.baconplayer .wrap{overflow:hidden;}
.baconplayer .progress{background:#E9EAEA;width:270px;height:10px;margin:13px 0 0 5px;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
.baconplayer .progress .inner-progress{background:#11b1e0;width:0;height:10px;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
.baconplayer .progress .loading-progress{background:#7d7d7d;width:0;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
.baconplayer .timing{float:right;color:#fff;margin-top:10px;padding-right:8px;}
#integration-branch{background:#ffb;border:1px solid #dd9;border-bottom:1px solid #ffb;padding:8px;color:#333;}
#integration-branch table td{padding:.5em .5em 0 0;}
#int-info img{position:relative;top:-.1em;}
#forkqueue .topper{overflow:hidden;}
#forkqueue #path{overflow:hidden;float:left;padding:0;margin-top:15px;}
#forkqueue .legend{font-size:100%;float:right;margin-top:22px;}
#forkqueue .legend .clean{border:1px solid #ccc;background:#DEFFDD url(/images/modules/forkqueue/bg_clean.png) 0 100% repeat-x;padding:.2em .4em;float:right;}
#forkqueue .legend .unclean{border:1px solid #ccc;background:#FFD9D9 url(/images/modules/forkqueue/bg_unclean.png) 0 100% repeat-x;padding:.2em .4em;float:right;margin-left:.8em;}
#forkqueue h2{font-size:120%;margin-bottom:.3em;margin-top:0;font-weight:normal;}
#forkqueue h2 a.branch{font-weight:bold;}
#forkqueue .queue-date{margin:-8px 0 20px 2px;color:#777;font-size:12px;font-style:italic;}
#forkqueue .queue-date abbr{font-style:italic;color:#444;}
#forkqueue .queue-date .js-fq-new-version{font-style:normal;}
#forkqueue table{width:100%;border-left:1px solid #ccc;border-right:1px solid #ccc;border-top:1px solid #ccc;margin-bottom:2em;}
#forkqueue table tr td{background-color:#eaf2f5;}
#forkqueue table tr.clean td{background:#DEFFDD url(/images/modules/forkqueue/bg_clean.png) 0 100% repeat-x;}
#forkqueue table tr.unclean td{background:#FFD9D9 url(/images/modules/forkqueue/bg_unclean.png) 0 100% repeat-x;}
#forkqueue table tr.unclean_failure td{background:#FFD9D9 url(/images/modules/forkqueue/bg_unclean.png) 0 100% repeat-x;border-bottom:none!important;}
#forkqueue table tr.failure td{background:#FFD9D9;}
#forkqueue table tr.failure td div.message{background:#FFECEC;padding:.5em;border:1px solid #FCC;margin-bottom:.3em;}
#forkqueue table th{font-weight:normal;border-bottom:1px solid #ccc;padding:.3em .6em;background-color:#eee;font-size:95%;text-align:left;}
#forkqueue table th select{margin-left:1em;}
#forkqueue table td{border-bottom:1px solid #ccc;padding:.3em .6em;}
#forkqueue table td.sha,#forkqueue table td.message{font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:80%;}
#forkqueue table td.checkbox{width:3%;}
#forkqueue table td.sha{width:6%;}
#forkqueue table td.human{font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:80%;width:4%;color:#888;}
#forkqueue table td.author{width:15%;font-weight:bold;}
#forkqueue table td.author img{vertical-align:middle;}
#forkqueue table td.message a{color:black;}
#forkqueue table td.message a:hover{text-decoration:underline;}
#forkqueue table td.date{width:12%;text-align:right;}
#forkqueue table td.author img{border:1px solid #ccc;padding:1px;background-color:white;}
#forkqueue table td.icons{width:3%;}
#forkqueue tr.failure .message h2{text-align:center;}
#forkqueue tr.failure .message p{font-size:130%;text-align:center;font-weight:bold;}
#forkqueue table.compare{border:none;margin:0;width:100%;}
#forkqueue table.compare td{padding:0;width:49.5%;border:none;background:none!important;vertical-align:top;}
#forkqueue table.compare td form{text-align:center;margin-bottom:.75em;}
#forkqueue table.compare td .confine{overflow:auto;width:32.75em;border:1px solid #ccc;}
#forkqueue table.compare td.spacer{width:1%;}
#forkqueue table.choice{margin:0;border:none;}
#forkqueue table.choice td{background:#f8f8f8!important;font-size:80%;vertical-align:middle;}
#forkqueue table.choice td.lines{width:1%;background-color:#ececec;color:#aaa;padding:1em .5em;border-right:1px solid #ddd;text-align:right;}
#forkqueue table.choice td.lines span{color:#9F5E5E;}
#forkqueue table.choice td.code{background-color:#f8f8ff!important;font-family:'Bitstream Vera Sans Mono','Courier',monospace;padding-left:1em;}
#forkqueue table.choice td.code span{color:#888;}
#forkqueue table.choice td.code a{color:#7C94AC;}
#forkqueue #finalize{text-align:center;}
#forkqueue .instructions{border:1px solid #ddd;background:#eee;padding:8px;color:#333;font-size:13px;margin:20px 0 8px 0;}
#header{margin:0 auto 0 auto;width:958px;height:91px;min-width:950px;}
#header .logo{display:block;position:relative;left:-6px;}
#header .logo.boring{left:20px;top:14px;}
#header .logo img{position:absolute;top:0;left:0;-webkit-transition:opacity .25s linear;-moz-transition:opacity .25s linear;}
#header .logo img.hover{opacity:0;}
#header .logo:hover img.hover{opacity:1;}
#header .logo img.default{opacity:1;}
#header .logo:hover img.default{opacity:0;}
ul.nav{margin:3px 0 0 0;white-space:nowrap;font-size:11px;}
ul.nav li{list-style-type:none;display:inline;margin:0 15px 0 0;}
ul.nav.logged_out{padding:8px 3px 8px 2px;font-size:12px;font-weight:bold;text-shadow:1px 1px 0 #fff;overflow:auto;}
ul.nav.logged_out li{float:left;margin:0;padding:0 11px 0 13px;background:url(/images/modules/header/nav-rule.png) 0 50% no-repeat;}
ul.nav.logged_out li:first-child{background:transparent;}
ul.nav.logged_out,.userbox{background:#f5f5f5;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fcfcfc',endColorstr='#ececec');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fcfcfc),to(#e8e8e8));background:-moz-linear-gradient(270deg,#fcfcfc,#ececec);border-color:#eee;border:1px solid #e9e9e9;border-bottom-color:#f5f5f5;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;-webkit-box-shadow:0 1px 1px rgba(0,0,0,0.2);-moz-box-shadow:0 1px 1px rgba(0,0,0,0.2);box-shadow:0 1px 1px rgba(0,0,0,0.2);}
.ie7 .userbox,.ie7 ul.nav.logged_out,.ie8 .userbox,.ie8 ul.nav.logged_out{border-bottom-color:#ddd;}
.userbox{float:right;padding:8px 5px 7px 10px;font-size:12px;border-top:none;-webkit-border-top-left-radius:0;-webkit-border-top-right-radius:0;-moz-border-radius-topleft:0;-moz-border-radius-topright:0;border-top-left-radius:0;border-top-right-radius:0;}
.userbox .avatarname{display:inline;padding-right:6px;font-weight:bold;}
.userbox .avatarname img{margin-top:-3px;margin-right:3px;vertical-align:middle;border:1px solid #fff;}
#header .userbox .avatarname a{color:#000;}
ul.usernav{display:inline;margin:0;font-weight:bold;}
ul.usernav li{list-style-type:none;display:inline;margin:0;padding:0 8px 0 9px;background:url(/images/modules/header/nav-rule.png) 0 50% no-repeat;}
ul.usernav li a{text-shadow:#fff 1px 1px 0;}
#header a.unread_count{display:inline-block;font-size:10px;margin-left:2px;padding:1px 5px;background:#ddd;color:#999;font-weight:bold;text-shadow:none;text-decoration:none;-webkit-border-radius:5px;-moz-border-radius:5px;}
#header a.unread_count.new{background-color:#4183c4;color:#fff;}
#header a.unread_count.notifications_count{display:none;}
#header a.unread_count.new.notifications_count{background-color:#666;display:inline-block;}
.topsearch{float:right;clear:right;margin-top:9px;width:500px;}
.topsearch form,.topsearch ul.nav{float:right;}
.topsearch form input.button{display:none;}
.topsearch form .advanced-search{display:inline-block;*display:none;width:16px;height:16px;text-indent:-9999px;background:url(/images/modules/header/advanced_search_icon.png) 0 0 no-repeat;opacity:.2;}
.topsearch form .advanced-search:hover{opacity:.5;}
.topsearch form input.search{font-size:16px;width:180px;}
.topsearch form input.search.notnative{width:149px;height:16px;padding:4px 10px 2px 21px;font-size:12px;border:none;background:url(/images/modules/header/search_field.gif) 0 -22px no-repeat;}
.topsearch form input.search.notnative.placeholder{background-position:0 0;}
#site_alert{background-color:#fcfcfc;border-bottom:1px solid #555;}
#site_alert p{text-align:center;font-weight:bold;color:#fff;background:#000;padding:8px 0;margin:0;}
.global-notice{padding:10px 0;border-top:2px solid #ff8a00;text-align:center;color:#fff;background:url(/images/modules/account/global_notice-background.gif) 0 100% repeat-x #c10000;}
.global-notice h2{margin:0;font-size:14px;}
.global-notice p{margin:0;}
.global-notice a{color:#fffb82;text-decoration:underline;}
.homehead .hero h1{background:#405a6a;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#839ba9',endColorstr='#405a6a');background:-webkit-gradient(linear,left top,left bottom,from(#839ba9),to(#405a6a));background:-moz-linear-gradient(top,#839ba9,#405a6a);}
.homehead .hero .textographic{color:#23566d;text-shadow:1px 1px 0 rgba(255,255,255,0.7);background-color:#e7eef1;-webkit-border-bottom-right-radius:3px;-webkit-border-bottom-left-radius:3px;-moz-border-radius-bottomright:3px;-moz-border-radius-bottomleft:3px;border-bottom-right-radius:3px;border-bottom-left-radius:3px;}
.homehead .hero .textographic a.repo{color:#23566d;}
.pagehead.homehead .hero h1{padding:10px 0 12px 0;text-align:center;font-size:30px;font-weight:normal;}
.homehead input.search{margin-left:10px;width:150px;padding:5px 5px 5px 25px;font-size:12px;font-family:helvetica,arial,freesans,clean,sans-serif;color:#666;background:url(/images/modules/home/search_icon.png) 5px 50% no-repeat #fff;border:1px solid #ccc;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.logos{margin:-5px 0 5px 0;text-align:center;}
.logos img{margin:0 8px;vertical-align:middle;}
.definitions{margin:25px 0 12px -19px;width:100%;padding:5px 19px;font-size:14px;color:#333;background:url(/images/modules/home/curly-rule-down.png) 0 0 no-repeat;}
.definitions .inner{margin-left:-19px;width:100%;padding:10px 19px;background:url(/images/modules/home/curly-rule.png) 0 100% no-repeat;}
.definitions h2{margin:0 0 -10px 0;font-family:Palatino,Georgia,"Times New Roman",serif;font-size:36px;font-weight:normal;color:#000;}
.definitions h2 em{position:relative;left:5px;top:-5px;color:#666;font-size:18px;font-style:normal;}
.whybetter{float:left;margin:0 0 22px 0;height:23px;padding:5px 5px 5px 8px;font-size:12px;line-height:23px;font-weight:bold;background:#f9f9e6;border:1px solid #ddd;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.whybetter select{margin:0 3px;}
.whybetter button{margin-left:5px;}
.signup-entice{padding:15px 0;text-align:center;font-size:16px;color:#666;}
.signup-entice p{margin-bottom:0;}
.signup-entice p a{font-weight:bold;}
.signup-button{display:inline-block;padding:15px 30px;color:#bed7e1;text-shadow:-1px -1px 0 rgba(0,0,0,0.25);font-size:12px;background:#286da3;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#50b7d1',endColorstr='#286da3');background:-webkit-gradient(linear,left top,left bottom,from(#50b7d1),to(#286da3));background:-moz-linear-gradient(top,#50b7d1,#286da3);border:1px solid #51a0b3;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;-webkit-box-shadow:0 1px 4px rgba(0,0,0,0.3);-moz-box-shadow:0 1px 4px rgba(0,0,0,0.3);box-shadow:0 1px 4px rgba(0,0,0,0.3);-webkit-font-smoothing:antialiased;}
a.signup-button:hover{text-decoration:none;background:#328fc9;background:-webkit-gradient(linear,0% 0,0% 100%,from(#66c7e5),to(#328fc9));background:-moz-linear-gradient(-90deg,#66c7e5,#328fc9);filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#66c7e5',endColorstr='#328fc9');}
.signup-button strong{display:block;color:#fff;font-size:20px;}
.signup-button em{font-weight:bold;font-style:normal;color:#c8ecff;}
.feature-overview{margin:25px 0;font-size:12px;color:#666;-webkit-font-smoothing:antialiased;}
.feature-overview strong{color:#333;}
.feature-overview h3{margin:0;font-size:16px;color:#000;}
.feature-overview h3 a{color:#000;}
.feature-overview p{margin:10px 0;}
.feature-overview p.more{font-weight:bold;}
#inbox{margin-top:10px;overflow:hidden;}
#inbox p{margin:0;}
#inbox h1{font-size:160%;margin-bottom:.5em;}
#inbox h1 a{font-size:70%;font-weight:normal;}
#inbox .actions{float:left;width:13em;margin-bottom:2em;}
#inbox .actions h1{color:white;}
#inbox .compose{border-bottom:1px solid #ddd;font-size:120%;padding-bottom:.5em;margin:.3em 0 1em 0;}
#inbox .actions .compose p a{text-decoration:none;}
#inbox .actions .compose p a span{text-decoration:underline;}
#inbox .boxes .new{font-weight:bold;}
#inbox .boxes li{padding-bottom:.4em;}
#inbox .actions p img{vertical-align:middle;}
#inbox .write{width:54em;float:right;clear:right;}
#inbox .write h1{border-bottom:1px solid #aaa;padding-bottom:.25em;margin:0;}
#inbox .write form{background-color:#EAF2F5;padding:.5em 1em 1em 1em;border-bottom:1px solid #ccc;}
#inbox .write .buttons .send{padding:0 2em;font-weight:bold;}
#inbox .write .buttons .cancel{padding:0 1em;}
#inbox .write .buttons-top{margin-bottom:.3em;}
#inbox .write .submits{margin-top:.7em;overflow:hidden;}
#inbox .write .submits .buttons-bottom{float:left;}
#inbox .write .submits .formatting{float:right;}
#inbox .write .field{overflow:hidden;margin:.5em 0;}
#inbox .write label{width:4em;float:left;text-align:right;padding-right:.3em;vertical-align:middle;line-height:1.7em;}
#inbox .write .field input{width:39.3em;border:1px solid #ccc;font-size:120%;padding:.2em;}
#inbox .write textarea{width:47em;border:1px solid #ccc;font-size:110%;padding:.2em;}
#inbox .list{width:54em;float:right;clear:right;}
#inbox .list h1{border-bottom:1px solid #aaa;padding-bottom:.25em;margin:0;}
#inbox .list .item{padding:1em 0 0 2.3em;overflow:hidden;border-bottom:1px solid #ccc;}
#inbox .list .unread{background-color:#eaf2f5!important;}
#inbox .list .item .body{overflow:hidden;padding:0 0 1em 0;}
#inbox .list .item .del{float:right;padding-right:.5em;}
#inbox .list .item .title{padding:0 0 .25em 0;font-weight:bold;}
#inbox .list .item .title span{background-color:#fff6a9;}
#inbox .list .item .gravatar{border:1px solid #d0d0d0;padding:2px;background-color:white;float:left;line-height:0;margin-right:.7em;}
#inbox .list .item .details .message a.subject{font-weight:bold;}
#inbox .list .item .details .message a.body{color:#23486b;}
#inbox .list .pull_request{background:url(/images/modules/inbox/pull_request.png) .5em 1em no-repeat;}
#inbox .list .unread.item{background:url(/images/modules/inbox/message.png) .5em 1em no-repeat;}
#inbox .list .item{background:url(/images/modules/inbox/read_message.png) .5em 1em no-repeat;}
#message{overflow:hidden;}
#message h1{font-size:160%;margin-bottom:.5em;}
#message h1 a{font-size:70%;font-weight:normal;}
#message .actions{float:left;width:13em;margin-bottom:2em;}
#message .actions h1{color:white;}
#message .compose{border-bottom:1px solid #ddd;font-size:120%;padding-bottom:.5em;margin:.3em 0 1em 0;}
#message .actions .compose p a{text-decoration:none;}
#message .actions .compose p a span{text-decoration:underline;}
#message .boxes .new{font-weight:bold;}
#message .boxes li{padding-bottom:.4em;}
#message .actions p img{vertical-align:middle;}
#message .envelope{float:right;width:54em;}
#message .envelope h1{border-bottom:1px solid #aaa;padding-bottom:.25em;margin:0;}
#message .envelope .header{padding:.75em 0 0 .5em;}
#message .envelope .header .gravatar{border:1px solid #d0d0d0;padding:2px;background-color:white;float:left;line-height:0;}
#message .envelope .header .info{padding:0 0 0 3.5em;}
#message .envelope .header .info .del{float:right;padding-right:.5em;}
#message .envelope .header .info .title{padding:0 0 .25em 0;font-weight:bold;}
#message .envelope .header .info .title.unread{background-color:#eaf2f5!important;}
#message .envelope .header .info .title span{background-color:#fff6a9;}
#message .envelope .body{margin:0 0 1.3em 4em;padding:0 0 1em 0;border-bottom:1px solid #ccc;}
#message .envelope .sent{background:#FFFBE2 none repeat scroll 0;border:1px solid #FFE222;padding:1em;font-weight:bold;}
#message .envelope .reply{margin:2em 0 0 4em;}
#message .envelope .reply .cancel{padding:0 1em;}
#message .envelope .reply label{font-size:110%;color:#666;display:block;clear:right;margin-top:1em;}
#message .envelope .reply textarea{width:99.8%;height:9em;border:1px solid #8496BA;margin-bottom:1em;}
#message .envelope .reply .controls{overflow:hidden;}
#message .envelope .reply .controls .submits{float:left;}
#message .envelope .reply .controls .formatting{float:right;}
.context-button{position:relative;vertical-align:middle;width:23px;height:16px;padding:0;}
.context-button .icon{position:absolute;padding:3px 3px;display:block;height:11px;width:18px;background:url(/images/modules/issues/context-button.png) no-repeat center 2px;}
.context-button:hover .icon,.context-button.selected .icon{background-position:center -19px;}
.context-pane{-webkit-box-shadow:0 0 13px rgba(0,0,0,0.31);position:absolute;background:#fff;border:1px solid #c1c1c1;width:300px;z-index:9;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.context-pane.edit-label-context{width:240px;}
.context-pane,.context-pane .body{-webkit-border-bottom-right-radius:4px;-webkit-border-bottom-left-radius:4px;-moz-border-radius-bottomright:4px;-moz-border-radius-bottomleft:4px;border-bottom-right-radius:4px;border-bottom-left-radius:4px;}
.context-pane .body{display:block;position:relative;padding:8px 10px;border-top:1px solid #ddd;}
.context-pane .title{font-weight:bold;font-size:14px;color:#111;text-shadow:1px 1px 0 rgba(255,255,255,1.0);padding:12px 10px 9px 10px;background:#f6f8f8;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f6f8f8',endColorstr='#e9eeee');background:-webkit-gradient(linear,left top,left bottom,from(#f6f8f8),to(#e9eeee));background:-moz-linear-gradient(top,#f6f8f8,#e9eeee);border-bottom:1px solid #f0f3f3;-webkit-border-top-left-radius:4px;-webkit-border-top-right-radius:4px;-moz-border-radius-topleft:4px;-moz-border-radius-topright:4px;border-top-left-radius:4px;border-top-right-radius:4px;}
.context-pane .close{display:block;float:right;margin-right:8px;margin-top:8px;width:8px;height:8px;background:url(/images/modules/issues/close-panel.png);}
.context-pane .close:hover{background-position:center -16px;}
.context-pane .body.pane-selector{padding:0;}
.pane-selector .selector-item{display:block;border-top:1px solid #eee;padding:8px 10px 8px 20px;background:url(/images/modules/context-pane/check.png) 5px 11px no-repeat;background-image:none;cursor:pointer;}
.pane-selector .selector-item.filterbar{padding-left:10px;background:none;}
.pane-selector .selector-item label{cursor:pointer;}
.pane-selector .selector-item.current,.pane-selector .selector-item:hover{background-color:#4f83c4;background-image:url(/images/modules/context-pane/check-white.png);}
.pane-selector .selector-item.filterbar:hover{background:none;}
.pane-selector .selector-item.clear:hover{background:#fff;}
.pane-selector>.selector-item:first-child{border-top:none;}
.pane-selector .selector-item.selected{background-image:url(/images/modules/context-pane/check.png);background-color:#fff;}
.pane-selector .selector-item.clear.selected{background-image:none;}
.pane-selector .selector-item:last-child{-webkit-border-bottom-right-radius:4px;-webkit-border-bottom-left-radius:4px;-moz-border-radius-bottomright:4px;-moz-border-radius-bottomleft:4px;border-bottom-right-radius:4px;border-bottom-left-radius:4px;}
.pane-selector .selector-item input[type=radio]{display:none;}
.pane-selector a.selector-item{text-decoration:none;}
.pane-selector .selector-item h4{margin:0;font-size:12px;font-weight:bold;color:#666;text-shadow:none;}
.pane-selector .selector-item.current h4,.pane-selector .selector-item:hover h4{color:#fff;text-shadow:0 0 2px rgba(0,0,0,0.6);}
.pane-selector .selector-item.selected h4{color:#333;text-shadow:none;}
.pane-selector .selector-item p,.pane-selector .selector-item.selected:hover p{margin:0;font-size:11px;color:#888;text-shadow:none;}
.pane-selector .selector-item:hover p{color:#fff;text-shadow:0 0 2px rgba(0,0,0,0.4);}
.pane-selector .selector-item.clear{font-size:12px;color:#999;}
.pane-selector .selector-item.clear .clear-text{display:block;margin-left:-20px;width:100%;padding:0 10px 0 20px;font-size:12px;font-weight:bold;color:#666;text-decoration:none;background:url(/images/modules/context-pane/clear.png) 7px 4px no-repeat;}
.pane-selector .selector-item.clear a.add{float:right;font-size:12px;font-weight:bold;}
.user-selector .avatar{position:relative;top:-2px;display:inline-block;padding:1px;border:1px solid #eee;vertical-align:middle;line-height:1px;}
.new-label input[type=text],.edit-label-context input[type=text]{padding:2px;width:97%;}
.new-label .custom-color,.edit-label-context .custom-color{margin:10px 0;}
.new-label .form-actions,.edit-label-context .form-actions{padding-right:0;}
.pane-selector.label-selector ul.labels{margin:0 10px 10px;}
#issues_next>.browser_header{position:relative;border-bottom:1px solid #ddd;}
#issues_next>.browser_header .search .spinner{vertical-align:middle;position:absolute;top:10px;left:-22px;margin-right:8px;}
#issues_next>.browser_header .search a{font-weight:200;color:#666;}
#issues_next>.browser_header .search .fieldwrap{display:inline-block;height:26px;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
#issues_next>.browser_header .search .fieldwrap>*{display:inline-block;}
#issues_next>.browser_header .search .fieldwrap.focused{outline:auto 5px -webkit-focus-ring-color;outline-offset:-2px;-moz-outline:-moz-mac-focusring solid 2px;-moz-outline-radius:0 5px 5px;-moz-outline-offset:0;}
#issues_next>.browser_header .search input{padding:5px 4px;font-size:12px;border:1px solid #d3d3d3;-webkit-border-top-left-radius:3px;-webkit-border-bottom-left-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-bottomleft:3px;border-top-left-radius:3px;border-bottom-left-radius:3px;}
#issues_next>.browser_header .search .minibutton{position:relative;top:-2px;margin-left:0;height:26px;padding-left:0;border-left:none;-webkit-border-radius:0;-moz-border-radius:0;border-radius:0;-webkit-border-top-right-radius:3px;-webkit-border-bottom-right-radius:3px;-moz-border-radius-topright:3px;-moz-border-radius-bottomright:3px;border-top-right-radius:3px;border-bottom-right-radius:3px;}
#issues_next>.browser_header .search .minibutton span{height:26px;width:16px;text-indent:-9999px;background:url(/images/modules/issues/search-icon.png) 50% 4px no-repeat;}
#issues_next>.browser_header .search .minibutton:hover span{background-position:50% -96px;}
#issues_next #issues_list .main .issues .issue .info span.label,#issues_next #show_issue .labels span.label{display:inline-block;font-size:11px;padding:1px 4px;-webkit-font-smoothing:antialiased;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;text-decoration:none;font-weight:bold;}
#issues_next .progress-bar{display:inline-block;position:relative;top:2px;margin-left:3px;height:15px;background:#e2e2e2;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#e2e2e2',endColorstr='#d8d8d8');background:-webkit-gradient(linear,left top,left bottom,from(#e2e2e2),to(#d8d8d8));background:-moz-linear-gradient(top,#e2e2e2,#d8d8d8);-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
#issues_next .progress-bar .progress{display:inline-block;height:15px;background:#8dcf16;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#8dcf16',endColorstr='#65bd10');background:-webkit-gradient(linear,left top,left bottom,from(#8dcf16),to(#65bd10));background:-moz-linear-gradient(top,#8dcf16,#65bd10);-webkit-border-top-left-radius:3px;-webkit-border-bottom-left-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-bottomleft:3px;border-top-left-radius:3px;border-bottom-left-radius:3px;}
#issues_next>.browser_header .search .autocomplete-results{position:absolute;border:1px solid #c1c1c1;-webkit-border-radius:6px;-moz-border-radius:6px;border-radius:6px;-webkit-box-shadow:0 0 13px rgba(0,0,0,0.31);-moz-box-shadow:0 0 13px rgba(0,0,0,0.31);box-shadow:0 0 13px rgba(0,0,0,0.31);z-index:99;background-color:#fff;width:250px;font-size:12px;}
#issues_next>.browser_header .search .autocomplete-results a{display:block;padding:5px;color:#000;}
#issues_next>.browser_header .search .autocomplete-results a:hover{text-decoration:none;}
#issues_next>.browser_header .search .autocomplete-results a.selected{background-color:#4183c4;color:#fff;}
#issues_next>.browser_header .search .autocomplete-results .header a{font-weight:bold;-webkit-border-top-left-radius:5px;-webkit-border-top-right-radius:5px;-moz-border-radius-topleft:5px;-moz-border-radius-topright:5px;border-top-left-radius:5px;border-top-right-radius:5px;}
#issues_next>.browser_header .search .autocomplete-results .header:last-child a,#issues_next>.browser_header .search .autocomplete-results .result-group tr:last-child th{-webkit-border-bottom-left-radius:5px;-moz-border-radius-bottomleft:5px;border-bottom-left-radius:5px;}
#issues_next>.browser_header .search .autocomplete-results .header:last-child a,#issues_next>.browser_header .search .autocomplete-results .result-group tr:last-child td,#issues_next>.browser_header .search .autocomplete-results .result-group tr:last-child a{-webkit-border-bottom-right-radius:5px;-moz-border-radius-bottomright:5px;border-bottom-right-radius:5px;}
#issues_next>.browser_header .search .autocomplete-results .result-group{width:100%;border-collapse:collapse;}
#issues_next>.browser_header .search .autocomplete-results .result-group a.selected{color:#fff;}
#issues_next>.browser_header .search .autocomplete-results .result-group th{width:68px;padding:5px;font-weight:normal;border-right:1px solid #ddd;font-size:11px;color:#999;vertical-align:top;text-align:right;}
#issues_next>.browser_header .search .autocomplete-results .result-group .title{font-weight:bold;}
#issues_next>.browser_header .search .autocomplete-results .result-group .milestone .info a{font-weight:bold;}
#issues_next>.browser_header .search .autocomplete-results .result-group .info .due_on,#issues_next>.browser_header .search .autocomplete-results .result-group .info .past_due{display:block;font-weight:normal;}
#issues_next>.browser_header .search .autocomplete-results .result-group .info .due_on{color:#666;}
#issues_next>.browser_header .search .autocomplete-results .result-group .info .past_due{color:#984646;}
#issues_next>.browser_header .search .autocomplete-results .result-group a.selected .due_on,#issues_next>.browser_header .search .autocomplete-results .result-group a.selected .past_due,#issues_next>.browser_header .search .autocomplete-results .result-group a.selected .number{color:#fff;}
#issues_next>.browser_header .search .autocomplete-results .result-group .info .number{color:#999;font-weight:bold;}
#issues_next>.browser_header .search .autocomplete-results .result-group .info .state{display:block;float:left;margin-right:5px;margin-top:3px;width:13px;height:9px;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;border-top-left-radius:2px 2px;border-top-right-radius:2px 2px;border-bottom-right-radius:2px 2px;border-bottom-left-radius:2px 2px;}
#issues_next>.browser_header .search .autocomplete-results .result-group .info .state.closed{background-color:#bd2c00;}
#issues_next>.browser_header .search .autocomplete-results .result-group .info .state.open{background-color:#6cc644;}
#issues_next>.browser_header a.minibutton{font-size:13px;padding:1px 1px 2px 3px;}
#issues_next>.browser_header ul.main_nav{font-size:14px;}
#issues_next>.browser_header ul.main_nav li{display:inline-block;cursor:pointer;}
#issues_next>.browser_header ul.main_nav li a{color:#666;text-decoration:none;padding:8px 12px;display:inline-block;margin-bottom:-1px;}
#issues_next>.browser_header ul.main_nav li:first-child a{padding-left:2px;}
#issues_next>.browser_header ul.main_nav li.selected:first-child a{padding-left:12px;}
#issues_next>.browser_header ul.main_nav li.selected{font-weight:bold;border-left:1px solid #ddd;border-top:1px solid #ddd;border-right:1px solid #ddd;-webkit-border-top-left-radius:3px;-webkit-border-top-right-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-topright:3px;border-top-left-radius:3px;border-top-right-radius:3px;background-color:#fff;}
#issues_next>.browser_header ul.main_nav li.selected a{color:#333;background-color:#fff;-webkit-border-top-left-radius:3px;-webkit-border-top-right-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-topright:3px;border-top-left-radius:3px;border-top-right-radius:3px;}
#issues_next>.browser_header ul.actions{float:right;margin-top:0;}
#issues_next>.browser_header ul.actions li{position:relative;display:inline-block;margin-left:5px;top:-4px;height:26px;padding:5px 0 7px 0;border:1px solid transparent;border-bottom:none;}
#issues_next>.browser_header ul.actions li.selected{padding-left:5px;padding-right:5px;background:#fff;border-color:#ddd;-webkit-border-top-left-radius:3px;-webkit-border-top-right-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-topright:3px;border-top-left-radius:3px;border-top-right-radius:3px;}
#issues_next ul.bignav{margin:0 0 -5px 0;}
#issues_next ul.bignav li{list-style-type:none;margin:0 0 5px 0;}
#issues_next ul.bignav li a{display:block;padding:8px 10px;font-size:14px;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
#issues_next ul.bignav li a:hover{text-decoration:none;background:#eee;}
#issues_next ul.bignav li a.selected{color:#fff;background:#4183c4;}
#issues_next ul.bignav li a .count{float:right;font-weight:bold;color:#777;}
#issues_next ul.bignav li a.selected .count{color:#fff;}
#issues_next #issues_list .label-context .labels .label .color{float:left;margin-right:5px;width:6px;height:14px;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
#issues_next #issues_list .sidebar{font-size:12px;}
#issues_next #issues_list .sidebar .milestone{margin:-5px 0 -5px;}
#issues_next .sidebar .milestone p{margin:0;color:#666;font-weight:bold;line-height:18px;}
#issues_next .sidebar .milestone p.noselect{color:#999;font-weight:normal;}
#issues_next #issues_list .sidebar .milestone .info-main{font-weight:bold;margin-bottom:3px;}
#issues_next #issues_list .sidebar .milestone .info-main .label{color:#b0b0b0;}
#issues_next #issues_list .sidebar .milestone .info-main .title{color:#414141;}
#issues_next #issues_list .sidebar .milestone .progress-bar{display:block;margin-left:0;margin-bottom:6px;}
#issues_next #issues_list .sidebar .milestone .info-secondary{font-size:11px;}
#issues_next #issues_list .sidebar .milestone .info-secondary .open{color:#818181;font-weight:bold;}
#issues_next #issues_list .sidebar .milestone .info-secondary .open{color:#959595;}
#issues_next #issues_list .sidebar .milestone .info a{display:inline;padding:0;color:inherit;}
#issues_next #issues_list .sidebar .milestone .info a:hover{background:none;text-decoration:underline;}
#issues_next #issues_list .sidebar .milestone .context-button{float:right;}
#issues_next #issues_list .pane-selector .milestones .selector-item:first-child{border-top:1px solid #EEE;}
#issues_next p.nolabels{margin:10px 0;font-size:11px;color:#666;}
#issues_next .labels .label{-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
#issues_next .labels .label a{color:#333;background:#fff;text-shadow:none;-webkit-border-radius:0;-moz-border-radius:0;border-radius:0;}
#issues_next .labels .label a:hover{background:#e3f6fc;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
#issues_next .labels .label a.selected,#issues_next .labels .label.zeroed a.selected{color:inherit;background:url(/images/modules/issues/label-close.png) 98% 5px no-repeat transparent;text-shadow:inherit;font-weight:bold;-webkit-font-smoothing:antialiased;}
#issues_next .labels .label a.selected:hover{background-position:98% -95px;}
#issues_next .labels .label .count{color:#333;}
#issues_next .labels .label a.selected .count{display:none;}
#issues_next .labels .label .color{display:block;float:left;margin-left:-5px;margin-right:4px;width:6px;height:14px;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
#issues_next .labels .label a:hover .color{-webkit-box-shadow:0 0 4px rgba(65,131,196,0.4);}
#issues_next .labels .label a.selected .color{display:none;}
#issues_next .labels .label.zeroed .count,#issues_next .labels .label.zeroed a{color:#999;}
#issues_next .sidebar .labels-editable a{display:inline;padding:0;color:#333;}
#issues_next .sidebar .labels-editable a:hover{background:transparent;}
#issues_next .sidebar .labels-editable .color{float:left;margin-right:5px;width:14px;height:14px;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
#issues_next .sidebar .labels-editable .color a{display:block;width:14px;height:14px;padding:0;margin:0;}
#issues_next .sidebar .labels-editable .delete a{float:right;background:transparent url("/images/icons/delete.png") 0 0 no-repeat;display:block;width:13px;height:13px;padding:0;margin:0;text-indent:-9999px;}
#issues_next .sidebar .labels-editable .delete a:hover{background-position:-15px 0;}
#issues_next .sidebar .labels-editable .delete a:active{background-position:-29px 0;}
#issues_next .sidebar .labels-editable .color a:hover,#issues_next .sidebar .labels-editable .color.selected a{background:transparent url("/images/icons/arrow-down.png") 1px 2px no-repeat;}
#issues_next .sidebar .labels-editable .label{padding-right:35px;background:#fff;color:#333;text-shadow:none;line-height:1.4em;padding:4px 0;}
#issues_next .sidebar .labels-editable .label{background:#fff;}
#issues_next .sidebar #manage-labels{width:100%;text-align:center;}
#issues_next #issues_list .main .filterbar ul.filters li{background-color:#f6f6f6;}
#issues_next #issues_list .main .filterbar ul.filters li.selected{background-color:#888;}
#issues_next #issues_list .main .actions{background:#fff;background:-moz-linear-gradient(top,#fff 0,#ecf0f1 100%);background:-webkit-gradient(linear,left top,left bottom,color-stop(0%,#fff),color-stop(100%,#ecf0f1));filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#ffffff',endColorstr='#ecf0f1',GradientType=0);margin:0;padding:.5em;font-size:11px;overflow:hidden;}
#issues_list .main .actions .buttons.deactivated .minibutton{opacity:.5;-moz-opacity:.5;filter:alpha(opacity=50);}
#issues_list .main .actions .buttons.activated .minibutton{opacity:1.0;-moz-opacity:1.0;filter:alpha(opacity=100);}
#issues_list .main .actions .buttons p.note{margin:0 0 0 5px;display:inline-block;font-size:11px;color:#9ca9a9;}
#issues_list .main .actions .buttons.activated p.note{display:none;}
#issues_next #issues_list .main .actions .pagination{float:right;margin:0;padding:0;height:23px;line-height:23px;font-weight:bold;}
#issues_next #issues_list .main .actions .buttons .btn-label,#issues_next #issues_list .main .actions .buttons .btn-assignee,#issues_next #issues_list .main .actions .buttons .btn-milestone{position:relative;padding-right:8px;}
#issues_next #issues_list .main .actions .buttons .btn-label span.icon,#issues_next #issues_list .main .actions .buttons .btn-assignee span.icon,#issues_next #issues_list .main .actions .buttons .btn-milestone span.icon{position:absolute;width:6px;height:6px;top:8px;right:8px;background:url(/images/modules/issues/down-arrow.png) right center no-repeat;}
#issues_next #issues_list .main .footerbar{overflow:hidden;}
#issues_next #issues_list .main .footerbar .pagination{background:none;float:right;padding:0;margin:0;}
#issues_next #issues_list .main .pagination>.disabled{display:none;}
#issues_next #issues_list .main .pagination span.current,#issues_next #issues_list .main .pagination a{border:0;background:none;color:inherit;margin:0;}
#issues_next #issues_list .main .pagination a{color:#4183C4;}
#issues_next #issues_list .main .issues{-webkit-user-select:none;-khtml-user-select:none;-moz-user-select:none;-o-user-select:none;user-select:none;}
#issues_next #issues_list .main .issues table{border:0;width:100%;}
#issues_next #issues_list .main .issues table td{vertical-align:top;padding:5px;border-bottom:1px solid #eaeaea;}
#issues_next #issues_list .main .issues .issue{background:none;border:0;color:#888;}
#issues_next #issues_list .main .issues .issue .wrapper{position:relative;padding:5px;}
#issues_next #issues_list .main .issues .issue.even{background-color:#fff;}
#issues_next #issues_list .main .issues .issue.odd{background-color:#f9f9f9;}
#issues_next #issues_list .main .issues .issue .read-status,#issues_next #issues_list .main .issues .issue.unread .read-status{width:10px;}
#issues_next #issues_list .main .issues .issue.unread .read-status{background:url(/images/modules/issues/unread.png) no-repeat center 10px;}
#issues_next #issues_list .main .issues .issue.read .read-status{background:url(/images/modules/issues/read.png) no-repeat center 10px;}
#issues_next #issues_list .main .issues .issue .select-toggle{width:12px;}
#issues_next #issues_list .main .issues .issue .select-toggle span{opacity:.5;filter:alpha(opacity=50);}
#issues_next #issues_list .main .issues .issue.selected .select-toggle span{opacity:1.0;filter:alpha(opacity=100);}
#issues_next #issues_list .main .issues .issue .number{width:20px;}
#issues_next #issues_list .main .issues .issue .info{margin-top:-1.45em;margin-left:5.5em;padding:0;}
#issues_next #issues_list .main .issues .issue .info h3{margin:0 25px 3px 0;font-size:13px;font-weight:bold;}
#issues_next #issues_list .main .issues .issue .info h3 a{color:#000;}
#issues_next #issues_list .main .issues .issue .info p{margin:-2px 0 0 0;font-size:11px;font-weight:200;}
#issues_next #issues_list .main .issues .issue .info p strong{font-weight:200;color:#333;}
#issues_next #issues_list .main .issues .issue .info p a{color:inherit;}
#issues_next #issues_list .main .issues .issue .info .comments,#issues_next #issues_list .main .issues .issue .info .pull-requests{float:right;height:16px;padding:0 0 0 18px;font-size:11px;font-weight:bold;color:#999;}
#issues_next #issues_list .main .issues .issue .info .comments{margin-left:1em;background:url(/images/modules/pulls/comment_icon.png) 0 50% no-repeat;}
#issues_next #issues_list .main .issues .issue .info .pull-requests{background:url(/images/modules/issues/pull-request-off.png) 0 50% no-repeat;}
#issues_next #issues_list .main .issues .issue .info .comments a,#issues_next #issues_list .main .issues .issue .info .pull-requests a{color:#bcbcbc;}
#issues_next #issues_list .main .issues .issue a.assignee-bit{display:block;position:absolute;right:0;top:0;width:20px;height:20px;text-decoration:none;border:1px solid #ddd;border-right:none;border-top:none;-webkit-border-bottom-left-radius:3px;-moz-border-radius-bottomleft:3px;border-bottom-left-radius:3px;}
#issues_next #issues_list .main .issues .issue a.assignee-bit.yours{background-color:#fcff00;}
#issues_next #issues_list .main .issues .issue .assignee-bit .assignee-wrapper img{margin:2px;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;line-height:1px;}
#issues_next #issues_list .main .issues .issue.closed{background:url(/images/modules/pulls/closed_back.gif) 0 0;}
#issues_next #issues_list .main .issues .issue h3 em.closed{position:absolute;top:5px;right:23px;padding:2px 5px;font-style:normal;font-size:11px;font-weight:bold;text-transform:uppercase;color:white;background:#999;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;border-top-left-radius:3px 3px;border-top-right-radius:3px 3px;border-bottom-right-radius:3px 3px;border-bottom-left-radius:3px 3px;}
#issues_next #issues_list .main .issues .issue.selected{background-color:#ffffef;}
#issues_next #issues_list .main .issues .issue.active{background:#ffc;}
#issues_next #issues_list .main .issues .issue .active-arrow{position:absolute;top:18px;left:-12px;width:6px;height:9px;opacity:0;background:url(/images/modules/pulls/active_bit.png) 0 0 no-repeat;-webkit-transition:opacity .1s linear;-moz-transition:opacity .1s linear;}
#issues_next #issues_list .main .issues .issue.active .active-arrow{opacity:1.0;-webkit-transition:opacity .25s linear;-moz-transition:opacity .25s linear;}
.columns.composer{margin-top:15px;}
.columns.composer .column.main{float:left;width:740px;}
.columns.composer .column.sidebar{float:right;width:160px;}
.composer .starting-comment{margin-bottom:15px;padding:3px;background:#eee;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.composer .starting-comment>.body{padding:10px;background:#fff;border:1px solid #ddd;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
.composer dl.form{margin:0;}
.composer dl.form input[type=text].title{font-size:20px;font-weight:bold;width:98%;color:#444;}
.composer .comment-form{margin:10px 0 0 0;padding:0;background:none;}
.composer .comment-form ul.tabs a.selected{background:#eee;}
.composer .new-comments .comment{padding:0;border:none;font-size:13px;}
.composer .new-comments .comment .cmeta{display:none;}
.composer .new-comments .comment .body{margin:10px 0 0 -10px;width:100%;padding:10px 10px 0 10px;border-top:1px solid #ddd;}
.composer .sidebar h3{margin:0 0 5px 0;font-size:12px;color:#666;border-bottom:1px solid #ddd;}
.composer .sidebar ul.labels li{cursor:pointer;}
.composer .sidebar ul.labels li{list-style-type:none;}
.composer .sidebar ul.labels .add{float:right;font-weight:bold;color:#999;}
.composer .sidebar ul.labels li:hover .add{color:#333;}
.composer .sidebar ul.labels li .selected .add{display:none;}
#issues_next .composer .sidebar ul.labels li a{padding:3px 0 3px 5px;font-size:12px;text-decoration:none;}
#issues_next .composer .sidebar .labels .label a.selected{background-position:98.5% 4px;}
#issues_next .composer dl.form.body{margin-top:25px;}
#issues_next #milestone_due_on{width:240px;}
#issues_next #show_issue #discussion_bucket{overflow:hidden;}
#issues_next #show_issue #discussion_bucket .discussion-stats{padding-top:20px;}
#issues_next #show_issue #discussion_bucket .discussion-stats .label-manager{text-align:left;font-weight:bold;font-size:12px;color:#636363;}
#issues_next #show_issue #discussion_bucket .discussion-stats .label-manager .context-button{float:right;}
#issues_next .context-pane.assignee-context .body,#issues_next .context-pane.assignee-assignment-context .body{max-height:350px;overflow-y:auto;}
#issues_next .context-pane.assignee-context .body input[type=text],#issues_next .context-pane.label-context .body input[type=text],#issues_next .context-pane.assignee-context .body input[type=text],#issues_next .context-pane.assignee-assignment-context .body input[type=text]{width:98%;padding:2px;margin:5px 0;-webkit-box-sizing:border-box;-moz-box-sizing:border-box;box-sizing:border-box;}
#issues_next #show_issue .discussion-stats .rule{margin:10px 0;}
#issues_next #show_issue .discussion-stats p{margin:10px 0;font-size:12px;color:#666;}
#issues_next #show_issue .discussion-stats p strong{color:#333;}
#issues_next #show_issue #discussion_bucket .discussion-stats .labels{text-align:left;padding-top:5px;}
#issues_next #show_issue #discussion_bucket .discussion-stats .labels .label{font-size:11px;display:block;margin-top:5px;padding:3px 3px 3px 5px;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;font-weight:bold;-webkit-font-smoothing:antialiased;}
#issues_next #show_issue #discussion_bucket .discussion-stats .labels .label .name{overflow:hidden;white-space:nowrap;text-overflow:ellipsis;display:block;}
#issues_next #show_issue .discussion-stats p.add-label{margin:7px 0 15px 0;font-size:11px;font-weight:bold;}
#issues_next #show_issue form.edit_issue{background:none;padding:0;margin-left:0;}
#issues_next #show_issue form.edit_issue input[type="text"]{margin:0;}
#issues_next #show_issue form.edit_issue select{border:1px solid #ddd;font-size:12px;width:240px;}
#issues_next .context-pane .body.label-selector{max-height:350px;overflow-y:auto;}
#issues_next #issues_search.browser{margin:15px 0;}
#issues_next #issues_search .sidebar .back{margin:0;font-weight:bold;}
#issues_next #issues_search .sidebar .back a{padding-left:12px;background:url(/images/modules/issues/back-arrow.png) 0 50% no-repeat;}
#issues_next #issues_search .sidebar .rule{margin:12px 0;}
#issues_next #issues_search .sidebar .filters .states{list-style:none;list-style-image:none;}
#issues_next #issues_search .sidebar .filters .states li{display:inline;margin-right:20px;}
#issues_next #issues_search .sidebar .filters .assignee{margin-top:15px;}
#issues_next #issues_search .sidebar .filters .assignee select{border:1px solid #ddd;font-size:13px;}
#issues_next #issues_search .main .results .issue-result{margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid #eee;}
#issues_next #issues_search .main .results em{background-color:#fffbb8;font-style:normal;font-weight:bold;padding:1px 1px;}
#issues_next #issues_search .main .results .group{margin-left:60px;}
#issues_next #issues_search .main .results .state{display:block;float:left;width:50px;padding:3px 0;font-size:12px;color:white;text-align:center;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;margin-right:10px;}
#issues_next #issues_search .main .results .state.open{background:#6CC644;}
#issues_next #issues_search .main .results .state.closed{background:#BD2C00;}
#issues_next #issues_search .main .results .number,#issues_next #issues_search .main .results .title{font-size:14px;font-weight:bold;}
#issues_next #issues_search .main .results .number{color:#999;}
#issues_next #issues_search .main .results .body{font-size:12px;margin-top:5px;color:#333;}
#issues_next #issues_search .main .results .comment{margin-top:5px;background:url(/images/modules/issues/search-comment-author-bit.png) 10px 19px no-repeat;}
#issues_next #issues_search .main .results .comment .author{color:#999;}
#issues_next #issues_search .main .results .comment .author b{color:#333;}
#issues_next #issues_search .main .results .comment .comment-body{padding:3px;background:#EEE;-moz-border-radius:3px;-webkit-border-radius:3px;border-radius:3px;margin-top:8px;}
#issues_next #issues_search .main .results .comment .comment-body .wrapper{background:white;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;border:1px solid #CACACA;padding:6px;}
#issues_next .browser-content{border-color:#d5d5d5;}
#issues_next .browser-content .context-loader{top:31px;}
#issues_next .browser-content .filterbar{position:relative;height:30px;background:url(/images/modules/issue_browser/topbar-background.gif) 0 0 repeat-x;border-bottom:1px solid #b4b4b4;}
#issues_next .filterbar ul.filters{position:absolute;bottom:0;left:4px;margin:0;}
#issues_next .filterbar ul.filters li{list-style-type:none;float:left;margin:0 5px 0 0;padding:0 8px;height:24px;line-height:25px;font-size:12px;font-weight:bold;color:#888;text-shadow:1px 1px 0 rgba(255,255,255,0.3);text-decoration:none;border:1px solid #cdcdcd;border-bottom-color:#cfcfcf;-webkit-border-top-left-radius:3px;-webkit-border-top-right-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-topright:3px;border-top-left-radius:3px;border-top-right-radius:3px;background:#e6e6e6;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#e6e6e6',endColorstr='#d5d5d5');background:-webkit-gradient(linear,left top,left bottom,from(#e6e6e6),to(#d5d5d5));background:-moz-linear-gradient(top,#e6e6e6,#d5d5d5);}
#issues_next .filterbar ul.filters li.selected{color:#333;border-color:#c2c2c2;border-bottom-color:#f0f0f0;background:#efefef;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#efefef',endColorstr='#e6e6e6');background:-webkit-gradient(linear,left top,left bottom,from(#efefef),to(#e6e6e6));background:-moz-linear-gradient(top,#efefef,#e6e6e6);}
#issues_next .filterbar ul.sorts{margin:5px 10px 0 0;height:18px;}
#issues_next .filterbar ul.sorts li{margin:0 0 0 10px;height:18px;line-height:18px;font-size:11px;border:1px solid transparent;-webkit-border-radius:9px;-moz-border-radius:9px;border-radius:9px;}
#issues_next .filterbar ul.sorts li.asc,#issues_next .filterbar ul.sorts li.desc{padding-right:10px;background-color:#e9e9e9;background-position:6px 7px;border:1px solid #bcbcbc;border-right-color:#d5d5d5;border-bottom-color:#e2e2e2;-webkit-box-shadow:inset 1px 1px 1px rgba(0,0,0,0.05);-moz-box-shadow:inset 1px 1px 1px rgba(0,0,0,0.05);box-shadow:inset 1px 1px 1px rgba(0,0,0,0.05);}
#issues_next .filterbar ul.sorts li.asc{background-position:6px -92px;}
#issues_next #milestone_list .column.sidebar .create .classy{margin-left:0;text-align:center;width:100%;}
ul.color-chooser{margin:8px 0;height:22px;}
ul.color-chooser li{list-style-type:none;margin:0 0 0 1px;float:left;width:26px;height:22px;opacity:.7;filter:alpha(opacity=70);}
ul.color-chooser li:first-child{width:29px;margin-left:0;-webkit-border-top-left-radius:3px;-webkit-border-bottom-left-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-bottomleft:3px;border-top-left-radius:3px;border-bottom-left-radius:3px;}
ul.color-chooser li:last-child{width:28px;-webkit-border-top-right-radius:3px;-webkit-border-bottom-right-radius:3px;-moz-border-radius-topright:3px;-moz-border-radius-bottomright:3px;border-top-right-radius:3px;border-bottom-right-radius:3px;}
ul.color-chooser li:hover,ul.color-chooser li.selected{opacity:1.0;filter:alpha(opacity=100);-webkit-box-shadow:0 0 5px #2466a7;-moz-box-shadow:0 0 5px #2466a7;box-shadow:0 0 5px #2466a7;}
ul.color-chooser label{margin:0;display:block;height:22px;text-indent:-9999px;cursor:pointer;}
ul.color-chooser .selected label{background:url(/images/modules/issues/color-chooser-check.png) 50% 50% no-repeat;}
.new-label input.namefield{width:208px;padding:3px 4px;}
.new-label .form-actions{margin-top:10px;padding-right:0;}
.new-label .form-actions p.optional{margin:0;padding-top:0;float:left;font-size:11px;}
#issues_next .starting-comment .infobar{margin:15px 0 0 -10px;width:100%;padding:10px 10px 8px 10px;color:#666;border:1px solid #e5e5e5;border-left:none;border-right:none;background:#f5f5f5;}
#issues_next .starting-comment .infobar p.assignee{margin:0;float:left;height:20px;line-height:20px;}
#issues_next .starting-comment .infobar p.assignee .avatar{float:none;margin:0;}
#issues_next .starting-comment .infobar p.assignee .avatar img{position:relative;top:-2px;margin-right:3px;vertical-align:middle;border-radius:3px;}
#issues_next .starting-comment .infobar a,#issues_next .starting-comment .infobar strong{color:#333;font-weight:bold;}
#issues_next .starting-comment .infobar p.milestone{float:right;margin:0;height:20px;line-height:20px;}
#issues_next .starting-comment .infobar p.milestone .progress-bar{width:220px;}
#issues_next .issue-head{margin-top:-3px;padding:13px 10px 7px 10px;border:1px solid #ddd;border-top:none;border-bottom:2px solid #d5d5d5;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
#issues_next .issue-head .back a{padding-left:12px;background:url(/images/modules/issues/back-arrow.png) 0 50% no-repeat;}
#issues_next .issue-head .number{float:right;font-size:14px;font-weight:bold;color:#999;}
#issues_next .issue-head .number strong{color:#666;}
#issues_next .issue-head p.back{margin:0;float:left;font-weight:bold;}
#issues_next p.clear-filters{margin:0 0 10px 0;color:#999;}
#issues_next p.clear-filters a{padding-left:20px;color:#999;font-weight:bold;background:url(/images/modules/issues/clear-x.png) 0 0 no-repeat;}
#issues_next p.clear-filters a:hover{color:#666;background-position:0 -100px;}
#issues_next .browser .keyboard-shortcuts{margin-top:1px;color:#999;}
.marketing .pagehead h1{font-size:30px;}
.marketing .pagehead p{margin:-5px 0 0 0;font-size:14px;color:#777;}
.marketing .pagehead ul.actions{margin-top:10px;}
.marketing h2{margin:15px 0 10px 0;font-size:18px;}
.marketing h2.subdued{font-size:16px;color:#666;}
.marketing h2 .secure{float:right;padding:4px 22px 0 0;font-size:11px;font-weight:bold;text-transform:uppercase;color:#000;background:url(/images/icons/private.png) 100% 50% no-repeat;}
p.read-it{margin:25px 0 0 0;color:#000;text-align:center;font-size:25px;font-weight:bold;}
.marketing .questions textarea{width:428px;padding:5px;height:200px;}
.marketing .questions dl.form input[type=text]{width:426px;}
.marketing .equacols .form-actions{margin-top:15px;margin-bottom:15px;}
.marketing .questions p{font-size:14px;color:#666;}
.marketing .questions h2{font-size:16px;margin:15px 0 -10px 0;}
ul.bottom-nav,.content ul.bottom-nav{margin:15px 0;padding:10px 0;border-top:1px solid #ddd;font-size:14px;}
ul.bottom-nav:after{content:".";display:block;height:0;clear:both;visibility:hidden;}
* html ul.bottom-nav{height:1%;}
ul.bottom-nav{display:inline-block;}
ul.bottom-nav{display:block;}
ul.bottom-nav li{list-style-type:none;}
ul.bottom-nav li.prev{float:left;}
ul.bottom-nav li.prev a{padding-left:14px;background:url(/images/modules/features/small-arrow.png) 0 -95px no-repeat;}
ul.bottom-nav li.next{float:right;}
ul.bottom-nav li.next a{padding-right:14px;background:url(/images/modules/features/small-arrow.png) 100% 5px no-repeat;}
.plan{margin:10px 0;padding:10px;-webkit-font-smoothing:antialiased;border:1px solid transparent;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.plan p{margin:0;font-size:12px;}
.plans-row{margin-top:-10px;margin-left:-25px;width:945px;}
.plans-row .plan{float:left;margin-left:25px;width:268px;text-shadow:1px 1px 0 rgba(255,255,255,0.8);}
.plans-row .plan .rule{margin:0;width:100%;padding:0 10px;margin-left:-10px;border-top:1px solid rgba(0,0,0,0.1);border-bottom:1px solid rgba(255,255,255,0.6);}
.plans-row.foured{width:940px;margin-left:-20px;}
.plans-row.foured .plan{width:193px;margin-left:20px;}
.plans-row .plan .button.classy{display:block;margin:2px 0;text-align:center;}
.plan h3{margin:-5px 0 2px 0;font-size:24px;}
.plan .price{float:right;}
.plan .price .amount{color:#000;}
.plan .price .symbol{position:relative;top:-5px;font-size:16px;opacity:.7;}
.plan .price .duration{font-size:14px;opacity:.5;}
.plan ul.bigpoints{margin:12px 0;padding:7px 9px;font-weight:bold;font-size:14px;color:#000;background:rgba(255,255,255,0.5);border:1px solid rgba(0,0,0,0.2);border-right-color:rgba(0,0,0,0.1);border-bottom-color:rgba(0,0,0,0.05);-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.plan ul.bigpoints li{list-style-type:none;margin:0;}
.plan ul.smallpoints{margin:-10px 0 0 0;}
.plan ul.smallpoints li{list-style-type:none;padding:5px 0;opacity:.6;border-top:1px solid rgba(0,0,0,0.15);}
.plan ul.smallpoints li:first-child{border-top:none;}
.plan.hplan{margin:20px 0;height:40px;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fafafa',endColorstr='#eeeeee');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fafafa),to(#eee));background:-moz-linear-gradient(270deg,#fafafa,#eee);border-color:#e1e1e1;}
.plan.final:hover{-webkit-box-shadow:none;-moz-box-shadow:none;box-shadow:none;}
.hplan .price{float:left;margin-right:12px;height:100%;padding:0 8px;font-weight:bold;background:#fff;border:1px solid #b6b69e;border-right-color:#e0dfcb;border-bottom-color:#f4f2d2;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.hplan .price .symbol{position:relative;top:-14px;color:#666;font-size:20px;}
.hplan .price .amount{position:relative;top:-4px;font-size:34px;color:#000;}
.hplan .price .duration{position:relative;top:-4px;color:#999;font-size:16px;}
.hplan .button{margin:1px 0 0 0;float:right;}
.hplan h3{margin:1px 0 0 0;font-size:16px;color:#000;text-shadow:1px 1px 0 rgba(255,255,255,0.8);}
.final h3{font-weight:normal;}
.hplan p{color:#666;color:rgba(0,0,0,0.6);text-shadow:1px 1px 0 rgba(255,255,255,0.8);}
.hplan p strong{color:#000;}
.plan.personal,.plan.micro.final,.plan.small.final,.plan.medium.final{background:#d9eff6;background:-webkit-gradient(linear,0% 0,0% 100%,from(#eaf5fa),to(#c5e8f1));background:-moz-linear-gradient(-90deg,#eaf5fa,#c5e8f1);filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#eaf5fa',endColorstr='#c5e8f1');border-color:#c4dce2;}
.plan.personal.leftmost{background:-webkit-gradient(linear,25% 0,0% 100%,from(#eaf5fa),to(#c5e8f1));background:-moz-linear-gradient(-112deg,#eaf5fa,#c5e8f1);}
.plan.personal.middle{background:-webkit-gradient(linear,0% 0,0% 100%,from(#eaf5fa),to(#c5e8f1));background:-moz-linear-gradient(-90deg,#eaf5fa,#c5e8f1);}
.plan.personal.rightmost{background:-webkit-gradient(linear,-25% 0,0% 100%,from(#eaf5fa),to(#c5e8f1));background:-moz-linear-gradient(-68deg,#eaf5fa,#c5e8f1);}
.plan.personal h3{color:#1a526b;}
.plan.business,.plan.large.final,.plan.mega.final,.plan.giga.final{background:#f1fef4;background:-webkit-gradient(linear,0% 0,0% 100%,from(#f1fef4),to(#c4e6bd));background:-moz-linear-gradient(-90deg,#f1fef4,#c4e6bd);filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f1fef4',endColorstr='#c4e6bd');border-color:#c7e2c4;}
.plan.business.leftmost{background:-webkit-gradient(linear,25% 0,0% 100%,from(#f1fef4),to(#c4e6bd));background:-moz-linear-gradient(-112deg,#f1fef4,#c4e6bd);}
.plan.business.middle{background:-webkit-gradient(linear,0% 0,0% 100%,from(#f1fef4),to(#c4e6bd));background:-moz-linear-gradient(-90deg,#f1fef4,#c4e6bd);}
.plan.business.rightmost{background:-webkit-gradient(linear,-25% 0,0% 100%,from(#f1fef4),to(#c4e6bd));background:-moz-linear-gradient(-68deg,#f1fef4,#c4e6bd);}
.plan.business h3{color:#1f5714;}
.plan.free{background:#fbf9da;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fefef3',endColorstr='#fbf8d4');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fefef3),to(#fbf8d4));background:-moz-linear-gradient(270deg,#fefef3,#fbf8d4);border-color:#e7e4c2;}
.plan.free:hover{border-color:#d6d2ac;}
.free p{color:#4e4d29;}
.plan.fi{margin-top:0;background:#333;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#616161',endColorstr='#0f0f0f');background:-webkit-gradient(linear,0% 0,0% 100%,from(#616161),to(#0f0f0f));background:-moz-linear-gradient(-90deg,#616161,#0f0f0f);border:none;}
.plan.fi:hover{-webkit-box-shadow:0 0 25px rgba(0,0,0,0.35);-moz-box-shadow:0 0 25px rgba(0,0,0,0.35);box-shadow:0 0 25px rgba(0,0,0,0.35);}
.fi .logo{float:left;margin-right:12px;height:31px;padding:4px 9px 4px 6px;line-height:40px;font-weight:bold;background:#fff;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.fi h3{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.5);}
.fi p{color:#999;text-shadow:-1px -1px 0 rgba(0,0,0,0.8);}
.fi .button{margin:1px 0 0 0;float:right;}
ul.plans-features{margin:25px 0 25px -20px;font-size:14px;}
ul.plans-features li{list-style-type:none;display:inline-block;margin:0 0 0 20px;padding-left:20px;font-weight:bold;color:#000;background:url(/images/modules/marketing/check.png) 0 50% no-repeat;}
ul.plans-features li.intro{font-weight:normal;color:#666;padding:0;background:transparent;}
.faqs{color:#666;font-size:14px;}
.faqs strong.highlight{color:#444;background:#fdffe0;}
.faqs h2{margin:30px 0 -10px 0;font-size:16px;color:#000;}
.faqs h2:first-child{margin-top:15px;}
.faqs a{font-weight:bold;}
.featured-brands{margin:20px 0;padding:5px 10px;background:#fefefe;background:-webkit-gradient(linear,0% 0,0% 100%,from(#fefefe),to(#f2f8fa));background:-moz-linear-gradient(-90deg,#fefefe,#f2f8fa);filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fefefe',endColorstr='#f2f8fa');border:1px solid #ddd;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;text-align:center;font-size:14px;color:#677a84;}
ul.selling-points{margin:25px 0;}
ul.selling-points li{list-style-type:none;margin:15px 0;padding-left:20px;font-weight:bold;font-size:14px;color:#000;background:url(/images/modules/marketing/check.png) 0 50% no-repeat;}
ul.cards{margin:0 0 10px 0!important;height:25px;}
ul.cards li{list-style-type:none;float:left;margin:0 7px 0 0!important;}
ul.cards li.text{position:relative;top:5px;font-size:11px;color:#999;}
ul.cards .card{float:left;width:39px;height:25px;text-indent:-9999px;background-position:0 0;background-repeat:no-repeat;}
ul.cards .card.disabled{background-position:0 -25px;opacity:.3;-moz-opacity:.3;filter:alpha(opacity=30);}
ul.cards .card.visa{background-image:url(/images/modules/pricing/card-visa.gif);}
ul.cards .card.master{background-image:url(/images/modules/pricing/card-mastercard.gif);}
ul.cards .card.american_express{background-image:url(/images/modules/pricing/card-amex.gif);}
ul.cards .card.discover{background-image:url(/images/modules/pricing/card-discover.gif);}
ul.cards .card.jcb{background-image:url(/images/modules/pricing/card-jcb.gif);}
ul.cards .card.diners_club{background-image:url(/images/modules/pricing/card-diners.gif);}
ol.steps{margin:15px 0;padding:6px 10px;font-size:12px;color:#000;background:#ebf6e5;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
ol.steps:after{content:".";display:block;height:0;clear:both;visibility:hidden;}
* html ol.steps{height:1%;}
ol.steps{display:inline-block;}
ol.steps{display:block;}
ol.steps li{list-style-type:none;float:left;margin:0 0 0 8px;padding-left:48px;background:url(/images/modules/steps/arrow.png) 0 50% no-repeat;}
ol.steps li:first-child{margin:0;padding:0;background:transparent;}
ol.steps li span{display:block;padding:4px 7px 3px 7px;opacity:.7;}
ol.steps li.current{font-weight:bold;}
ol.steps li.current span{background:#fff;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;border:1px solid rgba(0,0,0,0.2);border-right-color:rgba(0,0,0,0.1);border-bottom-color:rgba(0,0,0,0);opacity:1.0;}
ol.steps li.completed span{display:block;padding-left:18px;background:url(/images/modules/steps/check.png) 0 50% no-repeat;opacity:.5;}
.pagehead .hero{width:958px;padding:0;margin:-16px 0 15px -19px;}
.ie7 .pagehead .hero{margin-top:-21px;}
.pagehead .hero h1{position:relative;margin:0;height:auto;padding:5px 10px;font-size:16px;font-weight:bold;color:#fff;-webkit-font-smoothing:antialiased;letter-spacing:0;text-shadow:-1px -1px 0 rgba(0,0,0,0.2);-webkit-border-top-left-radius:3px;-webkit-border-top-right-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-topright:3px;border-top-left-radius:3px;border-top-right-radius:3px;-webkit-box-shadow:0 2px 0 rgba(0,0,0,0.15);}
.pagehead .hero h1 em{font-weight:normal;color:#fff;opacity:.75;}
.hero h1{display:block;background:#999;background:-webkit-gradient(linear,0% 0,0% 100%,from(#ddd),to(#999));background:-moz-linear-gradient(-90deg,#ddd,#999);filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#dddddd',endColorstr='#999999');}
.hero.golden h1{background:#ded356;background:-webkit-gradient(linear,0% 0,0% 100%,from(#ded356),to(#94890d));background:-moz-linear-gradient(-90deg,#ded356,#94890d);filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#ded356',endColorstr='#94890d');}
.hero.features-theme h1{background:#405a6a;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#829aa8',endColorstr='#405a6a');background:-webkit-gradient(linear,left top,left bottom,from(#829aa8),to(#405a6a));background:-moz-linear-gradient(top,#829aa8,#405a6a);}
.hero ul.subnav{position:relative;float:right;margin:-32px 10px 0 0;height:25px;z-index:5;}
.hero ul.subnav li{list-style-type:none;margin:0 0 0 10px;float:left;font-size:11px;font-weight:bold;}
.hero ul.subnav li a{display:block;height:23px;padding:0 8px;line-height:23px;color:#fff;color:rgba(255,255,255,0.8);border:1px solid transparent;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;text-decoration:none;-webkit-font-smoothing:antialiased;}
.hero ul.subnav li a:hover{color:#fff;background:rgba(0,0,0,0.2);}
.hero ul.subnav li a.selected{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);background:rgba(255,255,255,0.15);border-top-color:rgba(0,0,0,0.3);border-left-color:rgba(0,0,0,0.3);border-bottom-color:rgba(255,255,255,0.2);border-right-color:rgba(255,255,255,0.2);cursor:pointer;}
.hero img{-webkit-border-bottom-right-radius:4px;-webkit-border-bottom-left-radius:4px;-moz-border-radius-bottomright:4px;-moz-border-radius-bottomleft:4px;border-bottom-right-radius:4px;border-bottom-left-radius:4px;}
.hero .heroimage{position:relative;}
.hero p.photocredit{position:absolute;bottom:0;left:0;margin:0;padding:5px 10px;font-size:11px;font-weight:bold;color:#999;background:#000;-webkit-font-smoothing:antialiased;background:rgba(0,0,0,0.5);}
p.photocredit a{color:#999;}
.hero .textographic{padding:15px 10px;text-align:center;font-size:14px;color:#666;background:url(/images/modules/hero/textographic-border.png) 0 100% no-repeat #eee;}
.hero .textographic p{margin:0;}
.hero .screenographic{position:relative;padding:15px 10px 0;-webkit-border-bottom-right-radius:4px;-webkit-border-bottom-left-radius:4px;-moz-border-radius-bottomright:4px;-moz-border-radius-bottomleft:4px;border-bottom-right-radius:4px;border-bottom-left-radius:4px;background:#edf3f6;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#edf3f6',endColorstr='#d3e1e8');background:-webkit-gradient(linear,left top,left bottom,from(#edf3f6),to(#d3e1e8));background:-moz-linear-gradient(top,#edf3f6,#d3e1e8);}
.hero .screenographic:after{content:".";display:block;height:0;clear:both;visibility:hidden;}
* html .hero .screenographic{height:1%;}
.hero .screenographic{display:inline-block;}
.hero .screenographic{display:block;}
.screenographic .browsercap{float:left;margin:0 5px 0 -5px;width:540px;height:145px;padding:21px 23px 0 17px;background:url(/images/modules/features/hero_browser.png) 0 0 no-repeat;}
.screenographic .caption{float:right;margin:25px 13px 0 0;width:320px;padding:12px;font-size:14px;color:#555;background:#f8fcff;border:1px solid #d0d7da;border-right:none;border-bottom:none;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.screenographic .caption p{margin:0;}
.screenographic .bottom{position:absolute;left:0;bottom:0;width:100%;height:6px;background:url(/images/modules/features/screenographic-bottom.png);opacity:.07;filter:alpha(opacity=07);}
.screenographic.community img{margin:-14px 0 0 -10px;}
.hero .screenographic p.photocredit{color:#aaa;background:rgba(0,0,0,0.75);-webkit-border-bottom-left-radius:4px;-moz-border-radius-bottomleft:4px;border-bottom-left-radius:4px;}
.hero .screenographic p.photocredit a{color:#fff;}
.screenographic .bigcount{padding:10px 20px;color:#fff;white-space:nowrap;background:#1a2933;background:rgba(35,45,52,0.8);-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.screenographic .bigcount p.count{margin:-10px 0 0 0;font-size:50px;line-height:50px;text-shadow:0 0 10px rgba(0,0,0,0.8);}
.screenographic .bigcount p.subtext{margin:-5px 0 0 0;font-size:12px;font-weight:bold;text-align:center;color:#ccc;color:rgba(255,255,255,0.7);}
.screenographic.hosting{padding-top:20px;padding-bottom:22px;padding-right:15px;}
.screenographic.hosting .bigcount{float:left;margin:0 15px 0 5px;}
.screenographic.community .bigcount{display:none;position:absolute;top:30px;left:50%;}
.screenographic .floating-text h3{margin-top:2px;margin-bottom:0;font-size:18px;color:#2f424e;}
.screenographic .floating-text p{margin-top:0;margin-bottom:0;font-size:14px;color:#50585d;}
.wider .site{width:958px;}
.wider .pagehead{position:relative;margin-left:-6px;width:958px;padding-left:6px;padding-right:6px;}
.wider .pagehead .hero{margin-left:0;}
div.content{font-size:14px;color:#333;}
.content h2{margin:40px 0 -10px 0;font-size:18px;color:#000;}
.feature-content h2{margin:0 0 -10px 0;font-size:18px;}
.content h2:first-child,.content .rule+h2{margin-top:0;}
.content h3{color:#000;margin:1.5em 0 -0.5em 0;}
.content h3:first-child{margin-top:5px;}
.content .figure{margin:15px 0;padding:1px;border:1px solid #e5e5e5;}
.content .figure:first-child{margin-top:0;}
.content ul{margin:25px 0 25px 25px;}
.content ul ul{margin-top:10px;margin-bottom:10px;}
.miniprofile{margin:15px 0;}
.miniprofile h3{margin:0;font-size:16px;}
.miniprofile p{margin:0 0 10px 0;color:#666;}
.miniprofile .profile-link,.miniprofile .public-info{margin:2px 0;font-size:11px;color:#999;}
ul.checklist{margin:20px 0;font-size:12px;font-weight:bold;}
.miniprofile ul.checklist{margin:30px 0;}
ul.checklist li{list-style-type:none;margin:15px 0;padding-left:25px;background:url(/images/modules/marketing/check.png) 0 2px no-repeat;}
ul.dates{margin:20px 0;font-size:12px;}
ul.dates li{list-style-type:none;margin:15px 0;padding-left:25px;background:url(/images/modules/marketing/calendar.png) 0 2px no-repeat;}
ul.dates li strong{color:#000;display:block;}
.content .quote{margin:25px 30px;}
.sidebar .quote{margin:20px 0;}
.content .quote blockquote{margin:0;font-family:Georgia,Times,serif;font-style:italic;color:#666;}
.content .quote cite{display:block;font-size:12px;font-weight:bold;font-style:normal;color:#333;text-align:right;}
.popout{padding:10px;font-size:12px;color:#36361d;background:#e3f2d4;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.popout p{margin:0;line-height:1.5;}
.popout p+p{margin-top:10px;}
pre.terminal{padding:10px 10px 10px 23px;color:#fff;background:url(/images/modules/features/terminal_sign.png) 10px 50% no-repeat #333;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.wider .centered-graphic{text-align:center;padding-bottom:37px;background:url(/images/modules/features/centered-graphic-glow.gif) 50% 100% no-repeat;}
.centered-graphic h2{margin-top:20px;}
.centered-graphic p{color:#444;}
.big-notice{margin:15px 0;padding:5px 20px;background:#efe;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#eeffee',endColorstr='#bedebe');background:-webkit-gradient(linear,left top,left bottom,from(#efe),to(#bedebe));background:-moz-linear-gradient(top,#efe,#bedebe);border:1px solid #bedebe;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.big-notice h3{margin-bottom:-10px;}
.contact-notice{margin:15px 0;padding:5px 20px;background:#eee;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#eeeeee',endColorstr='#bebebe');background:-webkit-gradient(linear,left top,left bottom,from(#eee),to(#bebebe));background:-moz-linear-gradient(top,#eee,#bebebe);border:1px solid #bebebe;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.contact-notice h3{margin-bottom:-10px;}
ul.feature-tabs{position:relative;margin:15px 0;padding:0 2px 29px;background:url(/images/modules/features/curly_rule.png) 0 100% no-repeat;}
ul.feature-tabs li{list-style-type:none;position:relative;float:left;margin:0 0 0 30px;width:215px;height:150px;text-align:center;z-index:5;}
ul.feature-tabs li:first-child{margin-left:0;}
ul.feature-tabs li.highlight{position:absolute;bottom:5px;left:-1000px;margin:0;width:224px;height:97px;background:url(/images/modules/features/feature-tab-highlight.png);z-index:1;}
.feature-tabs a{text-decoration:none;}
.feature-tabs .arrow{position:absolute;top:35px;left:-25px;display:block;opacity:.4;width:22px;height:20px;background:url(/images/modules/features/arrow.png) 0 0 no-repeat;}
.feature-tabs li:first-child .arrow{display:none;}
.feature-tabs .tab-button{display:block;position:absolute;top:80px;left:0;width:100%;padding:15px 0;text-decoration:none;text-shadow:1px 1px 0 rgba(255,255,255,0.5);background:#fdfdfd;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fdfdfd',endColorstr='#eeeeee');background:-webkit-gradient(linear,left top,left bottom,from(#fdfdfd),to(#eee));background:-moz-linear-gradient(top,#fdfdfd,#eee);border:1px solid #e9e9e9;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;cursor:pointer;z-index:5;}
.feature-tabs a:hover .tab-button{border-color:#ddd;-webkit-box-shadow:0 0 10px rgba(65,131,196,0.3);-moz-box-shadow:0 0 10px rgba(65,131,196,0.3);box-shadow:0 0 10px rgba(65,131,196,0.3);}
.feature-tabs .tab-button h3{margin:0;font-size:14px;}
.feature-tabs .tab-button p{margin:0;color:#888;}
.feature-tabs a.selected{cursor:default;}
.feature-tabs a.selected .tab-button{background:#fdfdf6;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fdfdf6',endColorstr='#f1efcc');background:-webkit-gradient(linear,left top,left bottom,from(#fdfdf6),to(#f1efcc));background:-moz-linear-gradient(top,#fdfdf6,#f1efcc);-webkit-box-shadow:none;-moz-box-shadow:none;box-shadow:none;cursor:default;}
.feature-tabs .selected .tab-button h3{color:#000;}
.feature-tabs .selected .tab-button p{color:#666;}
.browsered{margin-bottom:-15px;width:460px;background:url(/images/modules/features/browsered_browser.png) 0 0 no-repeat;}
.browsered.mini{width:300px;background-image:url(/images/modules/features/browsered_browser-mini.png);}
.browsered .inner{padding:14px 16px 35px 13px;background:url(/images/modules/features/browsered_shadow.png) 0 100% no-repeat;}
.browsered.mini .inner{padding-top:10px;background-image:url(/images/modules/features/browsered_shadow-mini.png);}
.caption{margin-top:-5px;margin-bottom:30px;padding:18px 8px 8px;font-size:11px;color:#384141;background:url(/images/modules/features/caption_back.png) 50% 0 no-repeat;-webkit-border-bottom-right-radius:4px;-webkit-border-bottom-left-radius:4px;-moz-border-radius-bottomright:4px;-moz-border-radius-bottomleft:4px;border-bottom-right-radius:4px;border-bottom-left-radius:4px;}
.caption p{margin:0;}
.browsered+h3{margin-top:5px;}
.access-infographic{text-align:center;}
.access-infographic p{margin:10px 0;font-size:12px;font-weight:bold;color:#444;}
.access-infographic p.subtext{margin-top:-10px;font-weight:normal;font-size:11px;}
.access-infographic p.repo{height:80px;padding-top:12px;font-size:22px;color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.2);-webkit-font-smoothing:antialiased;background:url(/images/modules/features/infographics/hosting-access.png) 0 0 no-repeat;}
.access-infographic p.methods{margin-top:15px;margin-bottom:-5px;font-size:16px;color:#000;}
.access-infographic .sep{padding:0 5px;}
.instructor-bio{padding-left:150px;}
.instructor-bio img{float:left;margin-top:5px;margin-left:-150px;padding:1px;border:1px solid #ddd;}
.instructor-bio h2{margin-top:15px;}
.about-company{margin-top:30px;}
.about-company .main h2{margin-top:0;font-size:285%;line-height:1.2em;text-align:justify;}
.about-company .main p{font-size:125%;text-align:justify;}
.about-company .main .photo img{border:1px solid #ddd;padding:1px;}
.about-company .main .photo p{font-size:80%;color:gray;text-align:center;margin:3px 0;}
.about-company .sidebar{height:400px;background-color:#eee;border-radius:7px;-moz-border-radius:7px;-webkit-border-radius:7px;color:#444;border:1px solid #ddd;}
.about-company .sidebar h2{font-size:200%;text-align:center;font-weight:normal;}
.about-company .sidebar ul{list-style:none;margin-left:0;padding-left:1em;}
.about-company .sidebar ul li{padding:1em;font-size:1.2em;}
.about .person{overflow:auto;clear:both;}
.about .person img{float:left;margin-right:1em;padding:2px;border:1px solid #ddd;display:block;}
.about .person{margin-bottom:3em;}
.about .person .bio{float:left;width:32em;}
.about .person .tldr{color:#855;}
.about .person .tldr strong{font-style:italic;}
.about .person .bio h2{font-size:170%;}
.about .person .bio h2 a{color:#bdcedc;font-style:italic;font-weight:normal;font-size:95%;}
.about .person .bio .location{margin:5px 0 0 0;font-weight:bold;color:#ccc;}
.about .person .bio p{margin:.5em 0 0 0;text-align:justify;}
.about .person .quote{float:right;width:250px;font:20px "Times New Roman";font-style:italic;margin:3px 0 0 0;padding:8px 12px;background-color:#e7f4ff;position:relative;border-radius:7px;-moz-border-radius:7px;-webkit-border-radius:7px;}
.about .person .quote p{margin:0;}
.about .person .quote>b{position:absolute;top:-.3em;left:-.07em;font-size:500%;color:black;opacity:.1;}
.about .person .quote p>b{opacity:.3;padding-right:4px;}
#issues_next .column.sidebar .create button.classy{width:100%;margin-left:0;}
.browser-content .milestone{padding:10px 10px 10px 15px;background:#fff;border-bottom:1px solid #ddd;}
.browser-content .milestone.pastdue{background:url(/images/modules/issues/pastdue.gif) 0 0 no-repeat #fff;}
.browser-content .milestone h3{margin:5px 0 0 0;font-size:16px;}
.browser-content .milestone p.date{margin:5px 0 5px 0;font-size:14px;color:#666;}
.browser-content .milestone.notdue p.date{color:#999;}
.browser-content .milestone.pastdue p.date{font-weight:bold;color:#b90000;}
.browser-content .milestone .description{margin-top:10px;margin-bottom:-10px;width:100%;padding:1px 0 1px 0;border-top:1px solid #eee;font-size:12px;font-weight:300;color:#666;}
.browser-content .milestone .progress{float:right;margin-top:3px;width:390px;}
#issues_next .browser-content .milestone .progress-bar{display:block;margin:0;top:0;height:30px;}
#issues_next .browser-content .milestone .progress-bar .progress{display:block;float:none;height:30px;}
.progress-bar .percent{position:absolute;top:4px;left:7px;font-size:16px;font-weight:bold;color:#fff;text-shadow:0 0 2px rgba(0,0,0,0.7);}
.browser-content .milestone ul.meta{margin:0;font-size:11px;}
.browser-content .milestone ul.meta li{list-style-type:none;margin:0 0 0 15px;float:right;font-weight:bold;}
.browser-content .milestone ul.meta li.numbers{float:left;margin-left:0;color:#888;font-weight:normal;}
.equacols .column>.fieldgroup:first-child{margin-top:0;}
ul.fieldpills.usernames li img{margin-right:2px;padding:1px;background:#fff;border:1px solid #ddd;vertical-align:middle;}
ul.fieldpills.repos-pills>li{margin:0 0 5px 0;padding:3px 0 3px 28px;background-image:url(/images/icons/public.png) #fff!important;background-position:5px 50%!important;background-repeat:no-repeat;}
ul.fieldpills.repos-pills>li.private{background-image:url(/images/icons/private.png);background-color:#FFFEEB;}
ul.fieldpills.repos-pills>li.private.fork{background-image:url(/images/icons/private-fork.png);}
ul.fieldpills.repos-pills>li a em{margin-top:1px;display:block;font-size:11px;font-style:normal;font-weight:normal;color:#666;}
ul.grouplist{margin:15px 0 20px 0;border-top:1px solid #ddd;}
ul.grouplist>li{list-style-type:none;position:relative;padding:8px 0;border-bottom:1px solid #ddd;}
ul.grouplist .icontip{position:absolute;display:block;width:32px;height:32px;top:8px;left:0;}
ul.grouplist>li.iconed{padding-left:38px;}
ul.grouplist>li.org-icon{background:url(/images/modules/organizations/org_icon.gif) 0 0 no-repeat;}
ul.grouplist>li.admin.org-icon{background-position:0 -100px;}
ul.grouplist li h3{margin:0;font-size:16px;}
ul.grouplist li p{margin:-2px 0 0 0;font-size:12px;color:#999;}
ul.grouplist>li ul.actions{position:absolute;top:50%;right:0;margin:-12px 0 0 0;}
ul.grouplist>li ul.actions li{display:inline-block;margin:0 0 0 5px;}
#facebox .change-gravatar-email .gravatar{float:left;padding:2px;border:1px solid #DDD;}
#facebox .change-gravatar-email form{float:left;width:65%;padding-left:15px;}
#facebox .change-gravatar-email input{font-size:14px;width:85%;}
#facebox .change-gravatar-email button{margin-top:12px;margin-left:0;}
#facebox .change-gravatar-email .spinner{margin-left:10px;}
#facebox .change-gravatar-email .error{color:#900;font-weight:bold;}
.pagehead{position:relative;margin:-20px 0 10px -25px;width:920px;padding:20px 25px 0;background:url(/images/modules/pagehead/background-white.png) 0 0 no-repeat;}
.logged_out .pagehead{margin-top:-25px;}
.pagehead.mine,.pagehead.vis-private{background-image:url(/images/modules/pagehead/background-yellow.png?v2);}
.admin .pagehead{background-image:url(/images/modules/pagehead/background-green.png);}
.pagehead h1{margin:0 0 10px 0;font-size:20px;font-weight:normal;height:28px;line-height:28px;letter-spacing:-1px;text-shadow:1px 1px 0 #fff;color:#495961;}
.pagehead.dashboard h1{font-size:16px;height:22px;line-height:22px;}
.pagehead.userpage h1{margin-bottom:0;font-size:30px;height:54px;line-height:54px;font-weight:bold;}
.pagehead.repohead h1{color:#666;margin-bottom:15px;padding-left:23px;background-repeat:no-repeat;background-position:0 50%;}
.pagehead.repohead.vis-public h1{background-image:url(/images/icons/public.png);}
.pagehead.repohead.vis-private h1{background-image:url(/images/icons/private.png);}
.pagehead h1 a{color:#495961;}
.pagehead.repohead h1 a{color:#4183c4;}
.pagehead.repohead.mirror h1,.pagehead.repohead.fork h1{margin-top:-5px;margin-bottom:15px;height:auto;}
.pagehead.repohead h1 span.fork-flag,.pagehead.repohead h1 span.mirror-flag{display:block;margin-top:-5px;font-size:11px;letter-spacing:0;}
.pagehead.repohead.vis-public.fork h1{background-image:url(/images/icons/public-fork.png);}
.pagehead.repohead.vis-public.mirror h1{background-image:url(/images/icons/public-mirror.png);}
.pagehead.repohead.vis-private.fork h1{background-image:url(/images/icons/private-fork.png);}
.pagehead.repohead.vis-private.mirror h1{background-image:url(/images/icons/private-mirror.png);}
.pagehead h1 em{font-style:normal;font-weight:normal;color:#99a7af;}
.pagehead h1 em strong{color:#919ea6;}
.pagehead h1.avatared img{vertical-align:middle;position:relative;top:-2px;margin-right:5px;padding:2px;border:1px solid #ddd;}
.pagehead.shrunken h1.avatared img{top:-1px;padding:1px;}
.pagehead.shrunken h1.avatared span{letter-spacing:0;color:#808080;margin-left:.5em;font-size:.9em;}
.pagehead .title-actions-bar{overflow:hidden;height:35px;}
.pagehead ul.actions{margin:0;float:right;position:relative;top:-45px;right:0;}
.pagehead.repohead ul.actions{top:-45px;padding:5px 0 5px 20px;background:url(/images/modules/pagehead/actions_fade.png) 0 0 no-repeat;right:0;}
.pagehead.repohead.vis-private ul.actions{background-image:url(/images/modules/pagehead/actions_fade-yellow.png);}
.pagehead.dashboard ul.actions{position:absolute;top:15px;right:25px;}
.pagehead.userpage ul.actions{top:-39px;}
.pagehead ul.actions li{list-style-type:none;display:inline;font-size:11px;font-weight:bold;color:#333;margin:0 0 0 5px;}
.pagehead ul.actions li.text{padding:0 5px;}
.pagehead ul.actions a.feed{display:inline-block;height:16px;padding:6px 10px 4px 25px;line-height:16px;background:url(/images/icons/feed.png) 5px 50% no-repeat #fff;border:1px solid #eee;-moz-border-radius:3px;-webkit-border-radius:3px;}
.pagehead p.description{margin:-8px 0 10px 0;font-size:12px;color:#999;}
.pagehead ul.tabs{position:relative;margin:10px 0 0 0;height:26px;padding:6px 10px;background:url(/images/modules/pagehead/tab_background.gif?v2) 0 0 repeat-x;border:1px solid #ddd;-webkit-border-radius:5px;-moz-border-radius:5px;}
.subnavd .pagehead ul.tabs,.pagehead.repohead ul.tabs{-webkit-border-bottom-right-radius:0;-webkit-border-bottom-left-radius:0;-moz-border-radius-bottomright:0;-moz-border-radius-bottomleft:0;border-bottom:1px solid #ddd;}
.pagehead.emptyrepohead ul.tabs{-webkit-border-radius:5px;-moz-border-radius:5px;border-bottom:none;}
.pagehead ul.tabs li{list-style-type:none;margin:0;display:inline;}
.pagehead ul.tabs li a{float:left;margin-right:10px;height:26px;padding:0 8px;line-height:26px;font-size:14px;color:#666;text-shadow:1px 1px 0 rgba(255,255,255,0.7);-webkit-border-radius:4px;-moz-border-radius:4px;}
.pagehead ul.tabs li a:hover{color:#333;background-color:#ccc;text-decoration:none;}
.pagehead ul.tabs li a.selected{position:relative;top:-1px;font-weight:bold;color:#333;background:#fff;border:1px solid #ccc;border-right-color:#eee;border-bottom-color:#eee;}
.flash-messages{margin-top:-10px;margin-bottom:20px;}
.flash-messages .flash{position:relative;margin:1px auto 13px auto;width:854px;height:40px;padding:0 15px;line-height:40px;font-weight:bold;font-size:12px;color:#1d2b3d;background:url(/images/modules/flash/background.gif) 0 0 no-repeat;}
.flash-messages .flash-error{color:#900;background-image:url(/images/modules/flash/background-red.gif);}
.flash-messages .flash .close{display:block;position:absolute;top:50%;right:15px;margin-top:-9px;width:18px;height:18px;text-indent:-9999px;background:url(/images/modules/flash/close.png) 0 0 no-repeat;opacity:.5;cursor:pointer;}
.flash-messages .flash .close:hover{opacity:1.0;}
ol.steps+.flash-messages{margin-top:-15px;}
.subnav-bar{position:relative;height:30px;padding:0 10px;background:url(/images/modules/pagehead/subnav_background.gif) 0 0 repeat-x;border:1px solid #ddd;border-top:1px solid #fafafa;border-bottom:1px solid #d2d2d2;z-index:3;-webkit-border-bottom-right-radius:5px;-webkit-border-bottom-left-radius:5px;-moz-border-radius-bottomright:5px;-moz-border-radius-bottomleft:5px;}
.repohead .subnav-bar{-webkit-border-bottom-right-radius:0;-webkit-border-bottom-left-radius:0;-moz-border-radius-bottomright:0;-moz-border-radius-bottomleft:0;}
.repohead.shortdetails .subnav-bar{-webkit-border-bottom-right-radius:5px;-webkit-border-bottom-left-radius:5px;-moz-border-radius-bottomright:5px;-moz-border-radius-bottomleft:5px;}
.subnav-bar>ul{position:relative;margin:4px 0 0 -6px;}
.subnav-bar>ul>li{position:relative;list-style-type:none;float:left;margin-right:10px;}
.subnav-bar>ul>li>a{position:relative;display:block;height:15px;padding:3px 5px;font-size:11px;text-decoration:none;color:#666;border:1px solid transparent;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;z-index:5;}
.subnav-bar>ul>li>a.dropdown{padding-right:15px;background-image:url(/images/modules/pagehead/subnav_dropdown_arrow.png);background-position:100% -20px;background-repeat:no-repeat;}
.subnav-bar>ul>li:hover>a{color:#333;background-color:#f8f8f8;border-color:#ccc;}
.subnav-bar>ul>li>a.selected{color:#000;text-shadow:1px 1px 0 rgba(255,255,255,0.6);background:#ddd;font-weight:bold;border-color:#c5c5c5;border-right-color:#eee;border-bottom-color:#eee;cursor:default;}
.subnav-bar>ul>li:hover>a.dropdown{background-position:100% 0;border-color:#ccc;border-bottom-color:#e2e2e2;-webkit-border-radius:0;-moz-border-radius:0;}
.subnav-bar>ul>li>a.defunct{color:#999;background:transparent;border-color:transparent!important;cursor:default;}
.subnav-bar>ul>li>ul{display:none;position:absolute;top:22px;max-height:275px;background:#f8f8f8;border:1px solid #ccc;overflow:auto;z-index:4;}
.subnav-bar>ul>li:hover>ul{display:block;margin:0;min-width:180px;}
.subnav-bar>ul>li>ul>li{list-style-type:none;margin:0;border-top:1px solid #e2e2e2;font-size:11px;}
.subnav-bar>ul>li>ul>li:first-child{border-top:none;}
.subnav-bar>ul>li>ul>li>a,.subnav-bar>ul>li>ul>li>strong{padding:4px 5px;display:block;font-weight:normal;}
.subnav-bar>ul>li>ul>li>a{font-weight:bold;}
.subnav-bar>ul>li>ul>li>a:hover{text-decoration:none;background-color:#eee;}
.subnav-bar #repo-search-form{float:right;margin-top:6px;}
.subnav-bar #repo-search-form input{width:170px;}
.metabox-loader,.context-loader{position:absolute;top:0;left:50%;margin-left:-75px;width:110px;padding:10px 10px 10px 30px;font-weight:bold;font-size:12px;color:#666;background:url(/images/modules/pagehead/metabox_loader.gif) 10px 50% no-repeat #eee;border:1px solid #ddd;border-top:1px solid #fff;-webkit-border-radius:5px;-webkit-border-top-left-radius:0;-webkit-border-top-right-radius:0;-moz-border-radius:5px;-moz-border-radius-topleft:0;-moz-border-radius-topright:0;z-index:20;}
.metabox-loader{top:-1px;}
.pagehead ul.tabs li.contextswitch{position:absolute;right:0;top:0;height:26px;padding:6px 10px 6px 10px;font-size:11px;border-left:1px solid #ddd;background:url(/images/modules/pagehead/context_back-up.png?v2) 100% 0 no-repeat;-webkit-border-top-right-radius:5px;-webkit-border-bottom-right-radius:5px;-moz-border-radius-topright:5px;-moz-border-radius-bottomright:5px;border-top-right-radius:5px;border-bottom-right-radius:5px;}
.pagehead ul.tabs li.contextswitch.activated{background-image:url(/images/modules/pagehead/context_back-down.png?v2);-webkit-border-bottom-right-radius:0;-moz-border-radius-bottomright:0;border-bottom-right-radius:0;}
.pagehead ul.tabs li.contextswitch.nochoices{background-image:url(/images/modules/pagehead/context_back-plain.png?v2);}
.pagehead ul.tabs li.contextswitch .toggle{display:block;height:26px;line-height:28px;padding-right:15px;font-weight:bold;color:#666;cursor:pointer;}
.pagehead ul.tabs li.contextswitch.nochoices .toggle{padding-right:0;cursor:default;}
.pagehead ul.tabs li.contextswitch .toggle code{font-size:11px;}
.pagehead ul.tabs li.contextswitch .toggle em{font-style:normal;color:#999;}
.pagehead ul.tabs li.contextswitch.activated .toggle{color:#999;}
.pagehead ul.tabs li.contextswitch ul{display:none;margin:0;position:absolute;top:39px;right:-1px;background:#fff;border:1px solid #ccc;border-top:none;z-index:100;-moz-box-shadow:0 2px 2px rgba(0,0,0,0.1);-webkit-box-shadow:0 2px 2px rgba(0,0,0,0.1);}
.pagehead ul.tabs li.contextswitch.activated ul{display:block;}
.pagehead ul.tabs li.contextswitch ul li{margin:0;padding:0;display:block;}
.pagehead ul.tabs li.contextswitch ul li.current{position:relative;background:#f6f6f6;}
.pagehead ul.tabs li.contextswitch ul li>a.manage-orgs{height:25px;color:#999;background:url(/images/modules/organizations/context_icon.png) 95% 5px no-repeat transparent!important;}
.pagehead ul.tabs li.contextswitch ul li>a.manage-orgs:hover{background-position:95% -20px!important;color:#4183c4!important;}
.pagehead ul.tabs li.contextswitch ul li>a{float:none;display:block;margin:0;height:auto;min-width:200px;padding:3px 10px;white-space:nowrap;font-size:12px;font-weight:bold;color:#4183c4;border-top:1px solid #ddd;text-shadow:none;-webkit-border-radius:0;-moz-border-radius:0;}
.pagehead ul.tabs li.contextswitch ul li.manage{line-height:12px;}
.pagehead ul.tabs li.contextswitch ul li.manage a{font-size:11px;}
.pagehead ul.tabs li.contextswitch ul li strong{display:block;min-width:200px;padding:3px 10px;line-height:26px;font-size:12px;}
.pagehead ul.tabs li.contextswitch ul li:first-child a{border-top:none;}
.pagehead ul.tabs li.contextswitch ul li a em{font-weight:normal;font-style:normal;color:#999;}
.pagehead ul.tabs li.contextswitch ul li a:hover{background:#4183c4;color:#fff;}
.pagehead ul.tabs li.contextswitch ul li a:hover em{color:#8ac0f5;}
.subnav-bar #repo-search-form input.search.notnative{width:139px;height:15px;padding:3px 10px 1px 21px;font-size:11px;border:none;background:url(/images/modules/pagehead/repo_search.gif) 0 -19px no-repeat;}
.subnav-bar #repo-search-form input.search.notnative.placeholder{background-position:0 0;}
.profilecols ul.stats{margin:-8px 0 0 0;}
.profilecols ul.stats li{list-style-type:none;float:left;margin-right:30px;}
.profilecols ul.stats li strong{display:block;font-size:36px;font-weight:bold;color:#000;}
.profilecols ul.stats li span{display:block;margin-top:-10px;font-size:11px;color:#999;}
.profilecols ul.stats li a:hover{text-decoration:none;}
.profilecols ul.stats li a:hover strong,.profilecols ul.stats li a:hover span{color:#4183c4;text-decoration:none;}
.following{clear:both;margin-top:80px;}
.following h3{margin:0 0 5px 0;font-size:12px;}
.following h3 a{font-weight:normal;margin-left:5px;}
.following ul.avatars{margin:0;}
.following ul.avatars li{list-style-type:none;display:inline;margin:0 1px 0 0;}
.following ul.avatars li img{padding:1px;border:1px solid #ddd;}
.profilecols h2{position:relative;font-size:18px;margin:0 0 5px 0;}
.profilecols h2 em{font-style:normal;color:#999;}
.profilecols h2 .repo-filter{position:absolute;right:0;bottom:2px;}
.profilecols h2 .repo-filter input{width:176px;height:15px;line-height:15px;padding:2px 12px;background:url(/images/modules/repo_list/profile_filter_input.gif) 0 -19px no-repeat;border:none;}
.profilecols h2 .repo-filter input.native{width:200px;height:auto;padding:2px 5px;font-size:11px;background-image:none;}
.profilecols h2 .repo-filter input.placeholder{background-position:0 0;}
.profilecols h2 .repo-filter input:focus{background-position:0 -19px;}
.profilecols .noactions{margin:5px 0 0 0;padding:10px;color:#333;font-size:14px;font-weight:normal;text-align:center;background:#ffe;border:1px solid #ddd;}
.profilecols .noactions p{margin:0;line-height:1.2;text-shadow:1px 1px 0 #fff;}
h1.avatared .tooltipped{display:inline-block;}
.vcard dl{margin:5px 0 0 0;font-size:12px;}
.vcard dl:first-child{margin-top:0;}
.vcard dl dt{margin:0;float:left;width:115px;color:#999;}
.vcard dl dd{margin:0;}
.userrepos .users{float:left;width:560px;}
.userrepos .repos{float:right;width:340px;}
.userrepos ul.repo_list{margin:15px 0;border-top:1px solid #ddd;}
.userrepos ul.repo_list li{list-style-type:none;margin:0;padding:0 0 0 10px;background:url(/images/icons/public.png) 0 8px no-repeat #fff;border-bottom:1px solid #ddd;}
.userrepos ul.repo_list li a{display:block;padding:6px 10px 5px 10px;font-size:14px;background:url(/images/modules/repo_list/arrow-40.png) 97% 50% no-repeat;}
.userrepos ul.repo_list li a:hover{background-image:url(/images/modules/repo_list/arrow-80.png);}
.userrepos ul.repo_list li .repo{font-weight:bold;}
.organization-bit{float:right;margin-top:12px;min-width:34px;padding-top:28px;text-align:center;font-size:7px;text-transform:uppercase;letter-spacing:0;color:#999;background:url(/images/modules/organizations/profile_bit.png) 50% 0 no-repeat;}
ul.org-members{margin:5px 0;border-top:1px solid #ddd;}
ul.org-members li{position:relative;list-style-type:none;margin:0;height:32px;padding:5px 0 5px 42px;border-bottom:1px solid #ddd;}
.org-members .gravatar{float:left;margin-left:-42px;padding:1px;border:1px solid #ddd;}
.org-members .placeholder .gravatar{opacity:.5;}
.org-members h4{margin:-1px 0 0 0;font-size:16px;}
.org-members .placeholder h4 a{color:#999;}
.org-members h4 em{font-style:normal;font-weight:normal;color:#99a7af;}
.org-members p{margin:-4px 0 0 0;font-size:11px;color:#666;}
.org-members .minibutton{position:absolute;top:50%;right:0;margin-top:-12px;}
.mini-sidetabs{margin:15px 0;float:right;width:110px;text-align:right;border-right:1px solid #eee;}
.mini-sidetabs li{float:none;display:block;margin-top:10px;}
.mini-sidetabs li:first-child{margin-top:5px;}
.mini-sidetabs a{display:inline-block;height:24px;line-height:24px;padding:0 8px;font-size:12px;color:#999;text-decoration:none;}
.mini-sidetabs a.selected{position:relative;right:-1px;color:#333;text-shadow:0 1px 1px rgba(255,255,255,0.5);font-weight:bold;background:url(/images/modules/pagehead/breadcrumb_back.gif) 0 0 repeat-x;border:1px solid #d1d1d1;border-bottom-color:#bbb;border-right-color:#ccc;-webkit-border-top-left-radius:3px;-webkit-border-bottom-left-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-bottomleft:3px;border-top-left-radius:3px;border-bottom-left-radius:3px;}
.mini-sidetabs .icon{display:inline-block;position:relative;top:4px;width:16px;height:16px;opacity:.5;}
.mini-sidetabs a.selected .icon{opacity:1.0;}
.mini-sidetabs .discussion-icon{background:url(/images/modules/tabs/icon_discussion.png) 0 0 no-repeat;}
.mini-sidetabs .commits-icon{background:url(/images/modules/tabs/icon_commits.png) 0 0 no-repeat;}
.mini-sidetabs .fileschanged-icon{background:url(/images/modules/tabs/icon_fileschanged.png) 0 0 no-repeat;}
.mini-sidetabs-content{width:800px;float:left;}
.discussion-timeline-cols .main{float:left;width:660px;}
.discussion-timeline-cols .sidebar{float:right;width:240px;}
.discussion-timeline-cols ul.discussion-actions{float:right;margin:0;text-align:right;}
.discussion-timeline-cols ul.discussion-actions li{list-style-type:none;margin:-10px 0 0 5px;display:inline-block;}
.discussion-timeline{width:800px;}
.discussion-stats{float:right;width:100px;}
.discussion-timeline .breakout{width:920px;}
.discussion-timeline p.explain{margin:0;font-size:12px;}
.discussion-timeline h2{margin:20px 0;font-size:14px;}
.discussion-timeline h4{font-size:11px;color:#666;margin:5px 0 5px 0;}
.discussion-timeline .commits-condensed{margin-top:0;border:none;}
.discussion-timeline .commits-condensed span.gravatar{width:16px;height:16px;}
.discussion-timeline .commits-condensed .commit code a{font-size:11px;}
.discussion-timeline .commits-condensed td{padding-left:.5em;}
.discussion-timeline .commits-condensed td.author{padding-left:0;color:#666;}
.discussion-timeline .body .commits-compare-link{padding-left:.5em;}
.new-comments .commit-list-comment{border-bottom:none;}
.discussion-timeline pre.diff-excerpt{font-size:11px;background:#fafbfc;color:#888;padding:0;margin:0;overflow:auto;}
.discussion-timeline pre.diff-excerpt div{padding:0 3px;}
.discussion-timeline pre.diff-excerpt div.gc{color:#777;padding:3px 3px;}
.discussion-timeline .line-comments .clipper{width:714px;}
.discussion-stats{font-size:11px;text-align:center;}
.discussion-stats .state{display:block;padding:7px 10px;font-size:14px;font-weight:bold;color:#fff;text-align:center;background:#6cc644;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.discussion-stats ul.changes{margin:10px 0;padding-bottom:10px;border-bottom:1px solid #ddd;}
.discussion-stats ul.changes li{list-style-type:none;margin:10px 0 0;text-align:center;font-size:12px;color:#666;}
.discussion-stats ul.changes li:first-child{margin-top:0;}
.discussion-stats ul.changes li strong{color:#333;}
.discussion-stats ul.changes .addition{font-weight:bold;color:#309c00;}
.discussion-stats ul.changes .deletion{font-weight:bold;color:#bc0101;}
ul.userlist{margin:0;border-top:1px solid #ddd;}
ul.userlist li{list-style-type:none;margin:0;height:20px;padding:4px 0;line-height:20px;border-bottom:1px solid #ddd;}
ul.userlist li .gravatar{display:inline-block;margin-top:-2px;padding:1px;font-size:1px;background:#fff;border:1px solid #eee;vertical-align:middle;}
ul.userlist li a{display:inline-block;font-size:12px;font-weight:bold;color:#666;}
.pull-head{padding:10px;border:1px solid #f5f5f5;border-top:none;border-bottom:2px solid #eee;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.pull-description{font-size:14px;margin:0;color:#333;font-weight:300;}
.pull-description a{font-weight:bold;color:#000;}
.pull-description .commit-ref{margin:0 3px;position:relative;top:-1px;}
.pull-head .state,.action-bubble .state{float:left;padding:3px 10px;margin-top:-2px;margin-right:8px;font-size:12px;font-weight:bold;color:#fff;background:#6cc644;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.action-bubble .state{float:none;padding:3px 5px;font-size:11px;}
.pull-head .state-closed,.action-bubble .state-closed,.discussion-stats .state-closed{background-color:#bd2c00;}
.pull-head .number{float:right;font-size:16px;font-weight:bold;color:#666;}
.pull-head .number a{color:#666;}
ul.tab-actions{float:right;height:25px;margin:0 0 -25px 0;}
ul.tab-actions li{list-style-type:none;margin:0 0 0 5px;display:inline-block;font-size:11px;font-weight:bold;}
.new-comments .starting-comment{margin:0;background:#fff;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
.starting-comment .content-title{border-bottom:none;}
.starting-comment h2.content-title{margin:0 0 -10px;font-size:20px;}
.new-comments .starting-comment .body p.author{margin:10px 0 0;color:#666;font-size:12px;}
.starting-comment p.author a{font-weight:bold;color:#666;}
.new-comments .starting-comment .body{padding:0 10px;font-size:13px;background:#fff;}
.pull-participation{margin:-10px 0 0;padding-left:60px;font-size:13px;font-weight:300;color:#666;}
.pull-participation .avatar{position:relative;display:inline-block;height:24px;top:-2px;margin-right:3px;}
.pull-participation .avatar .overlay{position:absolute;top:0;left:0;}
.pull-participation .avatar img{vertical-align:middle;}
.pull-participation a{font-weight:bold;color:#666;}
.attached-pull{margin:10px 10px 10px 0;background:#f1f1f1;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fcfcfc',endColorstr='#eeeeee');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fcfcfc),to(#eee));background:-moz-linear-gradient(270deg,#fcfcfc,#eee);border:1px solid #ddd;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.attached-pull a{display:block;padding:8px 10px 7px 28px;color:#666;text-shadow:1px 1px 0 rgba(255,255,255,0.7);background:url(/images/modules/issues/pull_request_icon.png) 10px 50% no-repeat;}
.attached-pull a strong{color:#000;}
.browser{margin:20px 0;}
ul.bignav{margin:0 0 -5px 0;}
ul.bignav li{list-style-type:none;margin:0 0 5px 0;}
ul.bignav li a{display:block;padding:8px 10px;font-size:14px;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
ul.bignav li a:hover{text-decoration:none;background:#eee;}
ul.bignav li a.selected{color:#fff;background:#4183c4;}
ul.bignav li a .count{float:right;font-weight:bold;color:#777;}
ul.bignav li a.selected .count{color:#fff;}
.filterbox{margin:8px 0;padding:10px;background:#fafafb;border:1px solid #ddd;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.filterbox input{width:100%;}
ul.smallnav{margin:0;}
ul.smallnav li{list-style-type:none;margin:0 0 2px 0;}
ul.smallnav li a{display:block;padding:4px 10px;font-size:12px;white-space:nowrap;text-overflow:ellipsis;overflow:hidden;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
ul.smallnav li.zeroed a{color:#999;}
ul.smallnav li a:hover{text-decoration:none;background:#e3f6fc;}
ul.smallnav li a.selected{color:#fff;background:#4183c4;}
ul.smallnav li a .count{float:right;font-weight:bold;color:#777;}
ul.smallnav li.zeroed a .count{font-weight:normal;}
ul.smallnav li a.selected .count{color:#fff;}
.browser-title{margin:0 0 10px 0;}
.browser-title h2{margin:0;font-size:16px;}
.browser .keyboard-shortcuts{margin-top:-2px;}
.browser-content{position:relative;background:#f6f6f6;border:1px solid #ddd;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.browser-content .context-loader{top:25px;}
.browser-content .filterbar{height:24px;font-family:"Helvetica Neue",Helvetica,Arial,freesans;background:url(/images/modules/pagehead/breadcrumb_back.gif) 0 0 repeat-x;-webkit-border-top-right-radius:5px;-webkit-border-top-left-radius:5px;-moz-border-radius-topright:5px;-moz-border-radius-topright:5px;border-top-right-radius:5px;border-top-left-radius:5px;border-bottom:1px solid #bbb;}
.filterbar ul.filters{float:left;margin:4px 0 0 5px;}
.filterbar ul.filters li{list-style-type:none;float:left;margin-right:4px;height:14px;line-height:13px;padding:0 4px;font-size:10px;color:#666;background:#f6f6f6;border:1px solid #f6f6f6;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;cursor:pointer;-moz-user-select:none;-khtml-user-select:none;user-select:none;}
.filterbar ul.filters li.selected{font-weight:bold;color:#fff;text-shadow:1px 1px 0 rgba(0,0,0,0.3);-webkit-font-smoothing:antialiased;background:#888;border-color:#888;border-top-color:#666;border-left-color:#666;}
.filterbar ul.sorts{float:right;margin:0;}
.filterbar ul.sorts li{list-style-type:none;float:left;margin:0;padding:0 7px;height:24px;line-height:23px;font-size:10px;color:#666;cursor:pointer;-moz-user-select:none;-khtml-user-select:none;user-select:none;}
.filterbar ul.sorts li.asc,.filterbar ul.sorts li.desc{padding-left:15px;color:#333;font-weight:bold;background:#eee;background:rgba(255,255,255,0.5);border:1px solid #ddd;border-color:rgba(0,0,0,0.1);border-top:none;border-bottom:none;background-image:url(/images/modules/pulls/sort_arrow.png);background-position:6px 9px;background-repeat:no-repeat;}
.filterbar ul.sorts li.asc:last-child,.filterbar ul.sorts li.desc:last-child{border-right:none;}
.filterbar ul.sorts li.asc{background-position:6px -90px;}
.browser-content .paging{padding:5px;background:#fff;border-bottom:1px solid #ddd;}
.browser-content .button-pager{display:block;padding:5px 0;text-align:center;font-size:12px;font-weight:bold;text-shadow:1px 1px 0 #fff;text-decoration:none;border:1px solid #e4e9ef;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;background:#fdfdfe;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fdfdfe',endColorstr='#eff3f6');background:-webkit-gradient(linear,left top,left bottom,from(#fdfdfe),to(#eff3f6));background:-moz-linear-gradient(top,#fdfdfe,#eff3f6);}
.browser-content .button-pager:hover{border-color:#d9e1e8;background:#fafbfd;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fafbfd',endColorstr='#dee8f1');background:-webkit-gradient(linear,left top,left bottom,from(#fafbfd),to(#dee8f1));background:-moz-linear-gradient(top,#fafbfd,#dee8f1);}
.browser-content .footerbar{padding:7px 10px 8px 10px;font-size:11px;font-weight:bold;color:#777;}
.browser-content .footerbar p{margin:0;text-shadow:1px 1px 0 rgba(255,255,255,0.5);}
.browser .none,.browser .error{padding:30px;text-align:center;font-weight:bold;font-size:14px;color:#999;border-bottom:1px solid #ddd;}
.browser .error{color:#900;}
.browser .listing{position:relative;padding:10px 10px 12px 10px;color:#888;background:#fff;border-bottom:1px solid #eaeaea;}
.browser .listing.closed{background:url(/images/modules/pulls/closed_back.gif) 0 0;}
.browser .listing.active{background-color:#ffffef;}
.browser .listing .read-status{position:absolute;display:block;top:10px;left:0;width:4px;height:33px;background:#e6e6e6;}
.browser .unread .read-status{background:#4183c4;}
.browser .active-bit{position:absolute;top:22px;left:-12px;width:6px;height:9px;opacity:0;background:url(/images/modules/pulls/active_bit.png) 0 0 no-repeat;-webkit-transition:opacity .1s linear;-moz-transition:opacity .1s linear;}
.browser .listing.active .active-bit{opacity:1.0;-webkit-transition:opacity .25s linear;-moz-transition:opacity .25s linear;}
.browser .listing .number{float:right;padding:2px 7px;font-size:14px;font-weight:bold;color:#444;background:#eee;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
.browser .listing h3{margin:-2px 0 0 0;font-size:14px;color:#000;}
.browser .listing h3 a{color:#444;}
.browser .unread h3 a{color:#000;}
.browser .closed h3 a{color:#777;}
.browser .listing h3 em.closed{float:right;position:relative;top:2px;padding:2px 5px;font-style:normal;font-size:11px;text-transform:uppercase;color:#fff;background:#999;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.browser .listing p{margin:0;}
.browser .listing p a{color:#555;text-decoration:none;}
.browser .listing .meta{float:left;margin-top:4px;margin-bottom:-2px;height:16px;padding:4px 6px;line-height:14px;font-size:11px;color:#666;color:rgba(0,0,0,0.55);text-shadow:1px 1px 0 rgba(255,255,255,0.5);background:#eee;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.browser .listing.active .meta{background:#eeeedf;}
.browser .closed .meta{background:#eaeaea;}
.browser .listing .meta .gravatar{display:inline-block;vertical-align:bottom;padding:1px;font-size:1px;background:#fff;border:1px solid #ccc;}
.browser .listing .updated{float:left;margin:9px 0 0 8px;font-size:11px;color:#999;}
.browser .listing .comments,.browser .listing .pull-requests{float:right;margin-top:9px;height:16px;padding:0 0 0 18px;font-size:11px;font-weight:bold;color:#999;}
.browser .listing .comments{background:url(/images/modules/pulls/comment_icon.png) 0 50% no-repeat;}
.browser .listing .pull-requests{background:url(/images/modules/issues/pull-request-off.png) 0 50% no-repeat;}
.browser .listing .comments a{color:#666;}
.pull-form{margin:0;}
.pull-form textarea{height:200px;}
.pull-form input[type=text]{font-size:14px;padding:5px 5px;margin:0 0 5px 0;width:98%;color:#444;}
.pull-form-main .form-actions{margin-top:10px;}
.new-pull-form-error{margin:5px 0 10px 0;font-weight:bold;color:#A00;}
.pull-dest-repo{margin-top:0;}
.pull-dest-repo a{font-size:12px;font-weight:bold;padding:5px 0 5px 22px;}
.pull-dest-repo.public a{background:white url(/images/icons/public.png) no-repeat 0 4px;}
.pull-dest-repo.private a{background:white url(/images/icons/private.png) no-repeat 0 4px;}
.pull-dest-repo p{font-size:11px;color:#999;margin:5px 0 15px 0;}
.pull-heading .btn-change{float:right;margin:9px 10px 0 0;}
.new-pull-request .pull-tabs{clear:both;}
.new-pull-request.invalid .btn-change{display:none;}
.editor-expander{cursor:pointer;}
.range-editor{margin:15px 0 20px;background:url(/images/modules/compare/dotdotdot.gif) 50% 80px no-repeat;}
.range-editor .chooser-box{float:left;width:420px;}
.range-editor .chooser-box.head{float:right;}
.range-editor table.reposha{margin:15px 0 0 0;width:100%;border-spacing:0;border-collapse:collapse;}
.reposha td.repo{width:1%;white-space:nowrap;}
.reposha .repo .at{padding-right:5px;color:#666;}
.reposha .sha{text-align:left;}
.reposha input[type=text]{width:98%;font-family:Helvetica,Arial,freesans;font-size:12px;line-height:20px;color:#444;}
.range-editor .commit-preview .message,.range-editor .commit-preview p.error{margin:10px 0 0 0;background:#f7f8f9;border:1px solid #ddd;border-bottom:none;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.range-editor .form-actions{margin:10px 0 0;}
.avatar-bubble{margin:20px 0;padding-left:60px;background:url(/images/modules/comments/bubble-arrow.png) 51px 20px no-repeat;}
.avatar-bubble .avatar{position:relative;float:left;margin-left:-60px;}
.avatar-bubble .bubble{padding:3px;background:#eee;-moz-border-radius:3px;-webkit-border-radius:3px;border-radius:3px;}
.new-comments .bubble .comment{margin:0;}
.new-comments .bubble .commit-comment{margin-top:3px;}
.new-comments .bubble .commit-comment.thread-start{margin-top:0;}
.bubble .comment-form{margin:0;}
.avatar-bubble .form-actions{margin-top:10px;}
.bubble .file-box{margin-bottom:0;}
.bubble .action-bar{width:100%;padding:2px 3px 5px 3px;text-align:right;margin-left:-3px;border-bottom:1px solid #ccc;min-height:26px;}
.bubble .action-bar .minibutton:last-child{margin-right:2px;}
.bubble .action-bar h3{margin:5px 0 0 5px;float:left;font-size:13px;font-weight:bold;}
.mini-avatar-bubble{width:800px;background:url(/images/modules/comments/bubble-arrow-up.png) 14px 25px no-repeat;}
.mini-avatar-bubble .avatar{position:relative;display:inline-block;height:24px;top:-2px;margin-right:3px;}
.mini-avatar-bubble .bubble{padding:3px;background:#eee;-moz-border-radius:3px;-webkit-border-radius:3px;border-radius:3px;}
.mini-avatar-bubble p.action{margin:10px 0 10px 8px;height:24px;font-size:13px;font-weight:300;color:#333;}
.mini-avatar-bubble p.action a{font-weight:bold;color:#333;}
.mini-avatar-bubble p.action img{vertical-align:middle;}
.mini-avatar-bubble p.action em{font-style:normal;color:#999;}
.avatar-bubble .avatar .overlay,.mini-avatar-bubble .avatar .overlay,.action-bubble .avatar .overlay{position:absolute;top:0;left:0;}
.avatar .overlay.size-48{width:48px;height:48px;background:url(/images/modules/comments/rounded-avatar-48.png) 0 0 no-repeat;}
.avatar .overlay.size-24{width:24px;height:24px;background:url(/images/modules/comments/rounded-avatar-24.png) 0 0 no-repeat;}
.action-bubble{margin:20px 0;}
.action-bubble .action{float:left;line-height:24px;}
.action-bubble .bubble{font-size:13px;font-weight:300;}
.action-bubble .bubble strong{font-weight:bold;}
.action-bubble .state{display:inline-block;padding:0 5px;height:24px;line-height:25px;text-shadow:0 -1px -1px rgba(0,0,0,0.25);}
.action-bubble .avatar{position:relative;top:-2px;display:inline-block;height:24px;margin-right:3px;}
.action-bubble .avatar img{vertical-align:middle;}
.action-bubble a{color:#444;}
.action-bubble .bubble p{margin:0;line-height:26px;}
.merge-pr{margin:15px 0 0 0;padding-top:3px;border-top:1px solid #ddd;}
.merge-pr p.push-more{margin:10px 0;font-size:12px;color:#777;}
.merge-pr p.push-more code{color:#000;font-size:12px;}
.merge-pr p.push-more a{color:#333;font-weight:bold;}
.merge-pr .bubble{margin:10px 0;padding:3px;background:#eee;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.merge-pr .mergeable{padding:8px 10px 7px;border:1px solid #bac385;-webkit-border-radius:2px;-moz-border-radius:2px;border-radius:2px;}
.merge-pr .mergeable.checking{background:#f9f8a5;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f9f8a5',endColorstr='#f1f0a7');background:-webkit-gradient(linear,left top,left bottom,from(#f9f8a5),to(#f1f0a7));background:-moz-linear-gradient(top,#f9f8a5,#f1f0a7);}
.merge-pr .mergeable.clean{background:#9ee692;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#9ee692',endColorstr='#6eda62');background:-webkit-gradient(linear,left top,left bottom,from(#9ee692),to(#6eda62));background:-moz-linear-gradient(top,#9ee692,#6eda62);border-color:#8bc384;}
.merge-pr .mergeable.dirty{padding-top:10px;position:relative;background:#b7b7b7;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#b7b7b7',endColorstr='#939393');background:-webkit-gradient(linear,left top,left bottom,from(#b7b7b7),to(#939393));background:-moz-linear-gradient(top,#b7b7b7,#939393);border-color:#888;}
.merge-pr .mergeable.merging{background:#82bccd;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#82bccd',endColorstr='#589ab3');background:-webkit-gradient(linear,left top,left bottom,from(#82bccd),to(#589ab3));background:-moz-linear-gradient(top,#82bccd,#589ab3);border-color:#84acc3;border-bottom-color:#648192;-webkit-border-bottom-left-radius:0;-moz-border-radius-bottomleft:0;border-bottom-left-radius:0;-webkit-border-bottom-right-radius:0;-moz-border-radius-bottomright:0;border-bottom-right-radius:0;}
.merge-pr .mergeable.dirty .shade{position:absolute;top:0;left:0;width:100%;height:4px;background:url(/images/modules/pulls/dirty-shade.png) 0 0 repeat-x;}
.merge-pr .mergeable .info{float:left;margin:-6px 0 0 -8px;width:28px;height:29px;background:url(/images/modules/pulls/infotip.png) 0 0 no-repeat;cursor:pointer;}
.merge-pr .mergeable .info:hover{background-position:0 -100px;}
.merge-pr .mergeable .info.selected{background-position:0 -200px;}
.merge-pr p.message{margin:0;color:#6e6d32;text-shadow:1px 1px rgba(255,255,255,0.7);}
.merge-pr .mergeable.clean p.message{color:#0b5f00;font-weight:bold;text-shadow:1px 1px 0 rgba(255,255,255,0.4);}
.merge-pr .mergeable.dirty p.message{color:#fff;font-weight:bold;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);}
.merge-pr .mergeable.merging p.message{color:#fff;font-weight:bold;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);}
@-webkit-keyframes rotate{from{-webkit-transform:rotate(0deg);}
to{-webkit-transform:rotate(-360deg);}
}
.merge-pr p.message .spinner{display:inline-block;margin-right:1px;width:10px;height:10px;background:url(/images/icons/static-spinner.png) 0 0 no-repeat;-webkit-animation-name:rotate;-webkit-animation-duration:1.5s;-webkit-animation-iteration-count:infinite;-webkit-animation-timing-function:linear;}
.merge-pr .mergeable .minibutton{float:right;margin-top:-3px;margin-right:-5px;margin-left:15px;}
.merge-pr .mergeable .help{float:right;font-size:12px;color:#fff;}
.merge-pr .commit-preview{position:relative;display:table-row;}
.merge-pr .commit-preview .message{display:table-cell;width:561px;padding:10px 10px 8px 10px;vertical-align:top;background:#f6f9fa;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f6f9fa',endColorstr='#e7f0f3');background:-webkit-gradient(linear,left top,left bottom,from(#f6f9fa),to(#e7f0f3));background:-moz-linear-gradient(top,#f6f9fa,#e7f0f3);border:1px solid #bedce7;-webkit-border-bottom-right-radius:2px;-moz-border-radius-bottomright:2px;border-bottom-right-radius:2px;}
.merge-pr .commit-preview .message pre{color:#5b6f74;font-size:12px;}
.merge-pr .commit-preview .message textarea{margin-top:10px;width:100%;height:50px;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:12px;color:#666;}
.merge-pr .commit-preview .author{display:table-cell;width:190px;padding:10px;vertical-align:top;background:#d3e5eb;border:1px solid #bedce7;border-right:none;-webkit-border-bottom-left-radius:2px;-moz-border-radius-bottomleft:2px;border-bottom-left-radius:2px;}
.merge-pr .commit-preview .gravatar{float:left;margin-right:10px;padding:2px;line-height:1px;border:1px solid #bedce7;background-color:white;}
.merge-pr .commit-preview .name{position:relative;font-size:12px;}
.merge-pr .commit-preview a{color:#000;}
.merge-pr .commit-preview .author-text{position:absolute;top:0;right:6px;color:#5b6f74;}
.merge-pr .commit-preview .date{font-size:12px;color:#778589;}
.merge-help-context{width:470px;}
.merge-help-context p.intro{margin-top:5px;padding-bottom:10px;font-size:12px;color:#666;border-bottom:1px solid #ddd;}
.merge-help-context #url_box{overflow:auto;margin:0 0 10px 0;}
.merge-help-context .clippy-tooltip{float:right;}
.merge-help-context input.url-field{width:273px;}
.highlight{background:#fff;}
.highlight .c{color:#998;font-style:italic;}
.highlight .err{color:#a61717;background-color:#e3d2d2;}
.highlight .k{font-weight:bold;}
.highlight .o{font-weight:bold;}
.highlight .cm{color:#998;font-style:italic;}
.highlight .cp{color:#999;font-weight:bold;}
.highlight .c1{color:#998;font-style:italic;}
.highlight .cs{color:#999;font-weight:bold;font-style:italic;}
.highlight .gd{color:#000;background-color:#fdd;}
.highlight .gd .x{color:#000;background-color:#faa;}
.highlight .ge{font-style:italic;}
.highlight .gr{color:#a00;}
.highlight .gh{color:#999;}
.highlight .gi{color:#000;background-color:#dfd;}
.highlight .gi .x{color:#000;background-color:#afa;}
.highlight .go{color:#888;}
.highlight .gp{color:#555;}
.highlight .gs{font-weight:bold;}
.highlight .gu{color:#800080;font-weight:bold;}
.highlight .gt{color:#a00;}
.highlight .kc{font-weight:bold;}
.highlight .kd{font-weight:bold;}
.highlight .kp{font-weight:bold;}
.highlight .kr{font-weight:bold;}
.highlight .kt{color:#458;font-weight:bold;}
.highlight .m{color:#099;}
.highlight .s{color:#d14;}
.highlight .na{color:#008080;}
.highlight .nb{color:#0086B3;}
.highlight .nc{color:#458;font-weight:bold;}
.highlight .no{color:#008080;}
.highlight .ni{color:#800080;}
.highlight .ne{color:#900;font-weight:bold;}
.highlight .nf{color:#900;font-weight:bold;}
.highlight .nn{color:#555;}
.highlight .nt{color:#000080;}
.highlight .nv{color:#008080;}
.highlight .ow{font-weight:bold;}
.highlight .w{color:#bbb;}
.highlight .mf{color:#099;}
.highlight .mh{color:#099;}
.highlight .mi{color:#099;}
.highlight .mo{color:#099;}
.highlight .sb{color:#d14;}
.highlight .sc{color:#d14;}
.highlight .sd{color:#d14;}
.highlight .s2{color:#d14;}
.highlight .se{color:#d14;}
.highlight .sh{color:#d14;}
.highlight .si{color:#d14;}
.highlight .sx{color:#d14;}
.highlight .sr{color:#009926;}
.highlight .s1{color:#d14;}
.highlight .ss{color:#990073;}
.highlight .bp{color:#999;}
.highlight .vc{color:#008080;}
.highlight .vg{color:#008080;}
.highlight .vi{color:#008080;}
.highlight .il{color:#099;}
.type-csharp .highlight .k{color:#00F;}
.type-csharp .highlight .kt{color:#00F;}
.type-csharp .highlight .nf{color:#000;font-weight:normal;}
.type-csharp .highlight .nc{color:#2B91AF;}
.type-csharp .highlight .nn{color:#000;}
.type-csharp .highlight .s{color:#A31515;}
.type-csharp .highlight .sc{color:#A31515;}
#readme{font:13.34px helvetica,arial,freesans,clean,sans-serif;}
#readme.announce{margin:1em 0;}
#readme span.name{font-size:140%;padding:.8em 0;}
#readme div.plain,#readme div.wikistyle{background-color:#f8f8f8;padding:.7em;}
#readme.announce div.plain,#readme.announce div.wikistyle{border:1px solid #e9e9e9;}
#readme.blob div.plain,#readme.blob div.wikistyle{border-top:none;}
#readme div.plain pre{font-family:'Bitstream Vera Sans Mono','Courier',monospace;font-size:85%;color:#444;white-space:pre-wrap;word-wrap:break-word;width:74em;}
#missing-readme{font:13.34px helvetica,arial,freesans,clean,sans-serif;text-align:center;background-color:#ffc;padding:.7em;border:1px solid #ccc;}
#readme.rst .borderless,#readme.rst table.borderless td,#readme.rst table.borderless th{border:0;}
#readme.rst table.borderless td,#readme.rst table.borderless th{padding:0 .5em 0 0!important;}
#readme.rst .first{margin-top:0!important;}
#readme.rst .last,#readme.rst .with-subtitle{margin-bottom:0!important;}
#readme.rst .hidden{display:none;}
#readme.rst a.toc-backref{text-decoration:none;color:black;}
#readme.rst blockquote.epigraph{margin:2em 5em;}
#readme.rst dl.docutils dd{margin-bottom:.5em;}
#readme.rst div.abstract{margin:2em 5em;}
#readme.rst div.abstract p.topic-title{font-weight:bold;text-align:center;}
#readme.rst div.admonition,#readme.rst div.attention,#readme.rst div.caution,#readme.rst div.danger,#readme.rst div.error,#readme.rst div.hint,#readme.rst div.important,#readme.rst div.note,#readme.rst div.tip,#readme.rst div.warning{margin:2em;border:medium outset;padding:1em;}
#readme.rst div.admonition p.admonition-title,#readme.rst div.hint p.admonition-title,#readme.rst div.important p.admonition-title,#readme.rst div.note p.admonition-title,#readme.rst div.tip p.admonition-title{font-weight:bold;font-family:sans-serif;}
#readme.rst div.attention p.admonition-title,#readme.rst div.caution p.admonition-title,#readme.rst div.danger p.admonition-title,#readme.rst div.error p.admonition-title,#readme.rst div.warning p.admonition-title{color:red;font-weight:bold;font-family:sans-serif;}
#readme.rst div.dedication{margin:2em 5em;text-align:center;font-style:italic;}
#readme.rst div.dedication p.topic-title{font-weight:bold;font-style:normal;}
#readme.rst div.figure{margin-left:2em;margin-right:2em;}
#readme.rst div.footer,#readme.rst div.header{clear:both;font-size:smaller;}
#readme.rst div.line-block{display:block;margin-top:1em;margin-bottom:1em;}
#readme.rst div.line-block div.line-block{margin-top:0;margin-bottom:0;margin-left:1.5em;}
#readme.rst div.sidebar{margin:0 0 .5em 1em;border:medium outset;padding:1em;background-color:#ffe;width:40%;float:right;clear:right;}
#readme.rst div.sidebar p.rubric{font-family:sans-serif;font-size:medium;}
#readme.rst div.system-messages{margin:5em;}
#readme.rst div.system-messages h1{color:red;}
#readme.rst div.system-message{border:medium outset;padding:1em;}
#readme.rst div.system-message p.system-message-title{color:red;font-weight:bold;}
#readme.rst div.topic{margin:2em;}
#readme.rst h1.section-subtitle,#readme.rst h2.section-subtitle,#readme.rst h3.section-subtitle,#readme.rst h4.section-subtitle,#readme.rst h5.section-subtitle,#readme.rst h6.section-subtitle{margin-top:.4em;}
#readme.rst h1.title{text-align:center;}
#readme.rst h2.subtitle{text-align:center;}
#readme.rst hr.docutils{width:75%;}
#readme.rst img.align-left,#readme.rst .figure.align-left,#readme.rst object.align-left{clear:left;float:left;margin-right:1em;}
#readme.rst img.align-right,#readme.rst .figure.align-right,#readme.rst object.align-right{clear:right;float:right;margin-left:1em;}
#readme.rst img.align-center,#readme.rst .figure.align-center,#readme.rst object.align-center{display:block;margin-left:auto;margin-right:auto;}
#readme.rst .align-left{text-align:left;}
#readme.rst .align-center{clear:both;text-align:center;}
#readme.rst .align-right{text-align:right;}
#readme.rst div.align-right{text-align:left;}
#readme.rst ol.simple,#readme.rst ul.simple{margin-bottom:1em;}
#readme.rst ol.arabic{list-style:decimal;}
#readme.rst ol.loweralpha{list-style:lower-alpha;}
#readme.rst ol.upperalpha{list-style:upper-alpha;}
#readme.rst ol.lowerroman{list-style:lower-roman;}
#readme.rst ol.upperroman{list-style:upper-roman;}
#readme.rst p.attribution{text-align:right;margin-left:50%;}
#readme.rst p.caption{font-style:italic;}
#readme.rst p.credits{font-style:italic;font-size:smaller;}
#readme.rst p.label{white-space:nowrap;}
#readme.rst p.rubric{font-weight:bold;font-size:larger;color:maroon;text-align:center;}
#readme.rst p.sidebar-title{font-family:sans-serif;font-weight:bold;font-size:larger;}
#readme.rst p.sidebar-subtitle{font-family:sans-serif;font-weight:bold;}
#readme.rst p.topic-title{font-weight:bold;}
#readme.rst pre.address{margin-bottom:0;margin-top:0;font:inherit;}
#readme.rst pre.literal-block,#readme.rst pre.doctest-block{margin-left:2em;margin-right:2em;}
#readme.rst span.classifier{font-family:sans-serif;font-style:oblique;}
#readme.rst span.classifier-delimiter{font-family:sans-serif;font-weight:bold;}
#readme.rst span.interpreted{font-family:sans-serif;}
#readme.rst span.option{white-space:nowrap;}
#readme.rst span.pre{white-space:pre;}
#readme.rst span.problematic{color:red;}
#readme.rst span.section-subtitle{font-size:80%;}
#readme.rst table.citation{border-left:solid 1px gray;margin-left:1px;}
#readme.rst table.docinfo{margin:2em 4em;}
#readme.rst table.docutils{margin-top:.5em;margin-bottom:.5em;}
#readme.rst table.footnote{border-left:solid 1px black;margin-left:1px;}
#readme.rst table.docutils td,#readme.rst table.docutils th,#readme.rst table.docinfo td,#readme.rst table.docinfo th{padding-left:.5em;padding-right:.5em;vertical-align:top;}
#readme.rst table.docutils th.field-name,#readme.rst table.docinfo th.docinfo-name{font-weight:bold;text-align:left;white-space:nowrap;padding-left:0;}
#readme.rst h1 tt.docutils,#readme.rst h2 tt.docutils,#readme.rst h3 tt.docutils,#readme.rst h4 tt.docutils,#readme.rst h5 tt.docutils,#readme.rst h6 tt.docutils{font-size:100%;}
#readme.rst ul.auto-toc{list-style-type:none;}
#repos{margin-bottom:1em;}
#repos h1{font-size:160%;}
#repos h1 a{font-size:70%;font-weight:normal;}
#repos .hint{font-style:italic;color:#888;margin:.3em 0;}
#repos .repo{margin:1em 0;padding:.1em .5em .1em .5em;}
#repos .public{border:1px solid #d8d8d8;background-color:#f0f0f0;}
#repos .private{border:1px solid #f7ca75;background-color:#fffeeb;}
#repos .repo .title{overflow:hidden;}
#repos .repo .title .path{float:left;font-size:140%;}
#repos .repo .title .path img{vertical-align:middle;}
#repos .repo .title .path .button{margin-left:.25em;vertical-align:-12%;}
#repos .repo .title .path span a{font-size:75%;font-weight:normal;}
#repos .repo .title .security{float:right;text-align:right;font-weight:bold;padding-top:.5em;}
#repos .repo .title .security *{vertical-align:middle;}
#repos .repo .title .security img{position:relative;top:-1px;}
#repos .repo .title .flexipill{float:right;padding-top:.3em;margin-right:.5em;}
#repos .repo .title .flexipill a{color:black;}
#repos .repo .title .flexipill .middle{background:url(/images/modules/repos/pills/middle.png) 0 0 repeat-x;padding:0 0 0 .3em;}
#repos .repo .title .flexipill .middle span{position:relative;top:.1em;font-size:95%;}
#repos .repo .meta{margin:.2em 0 0 0;overflow:hidden;}
#repos .repo .meta table{float:left;max-width:48em;}
#repos .repo .meta table td *{vertical-align:middle;}
#repos .repo .meta table td.label{color:#888;padding-right:.25em;vertical-align:bottom;}
#repos .repo .meta table td span.editarea input{margin-top:.5em;margin-right:.5em;}
#repos .repo .meta table td textarea{display:block;clear:right;}
#repos .repo .meta table td.url{color:#4183c4;}
#repos .repo .meta table td.blank{color:#bbb;}
#repos .repo .pledgie{float:right;}
#repos .repo .commit{border:1px solid #bedce7;margin-top:.5em;padding:0 .5em .5em .5em;background:#eaf2f5 url(/images/modules/commit/bg_gradient.gif) 0 100% repeat-x;overflow:hidden;}
#repos .repo .commit .actor{float:left;margin-top:.5em;}
#repos .repo .commit .actor .gravatar{border:1px solid #d0d0d0;padding:2px;background-color:white;float:left;line-height:0;margin-right:.7em;}
#repos .repo .commit .actor .name{line-height:1.5em;}
#repos .repo .commit .actor .name span{color:#888;font-size:90%;}
#repos .repo .commit .actor .date{color:#888;font-size:90%;line-height:1em;}
#repos .repo .commit .message{float:left;padding:.5em 0 .5em .5em;margin-left:2em;border-left:1px solid #bedce7;}
#repos .repo .commit .machine{float:right;width:30em;padding:.5em 0 .5em .5em;border-left:1px solid #bedce7;color:#808080;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:85%;line-height:1.5em;}
#repos .repo .diffs{margin-top:.5em;}
#repos .repo .diffs .diff *{vertical-align:middle;}
#repos .repo .diffs .diff img{position:relative;top:-1px;}
.search-match{background:#fffccc;font-weight:bold;}
#import_repo .import_step{border:1px solid #888;background:#fff;margin:15px 0;padding:15px;}
#import_repo .failed_import{background:#fdd;}
#import_repo h3{margin-bottom:.8em;}
#import_repo ul{margin-bottom:2em;}
#import_repo ul li{margin:0 0 .8em 1.5em;}
#import_repo #authors-list{width:100%;}
#import_repo #authors-list th{padding-left:.5em;}
#import_repo #authors-list input{width:100%;}
ul.repositories{margin:0;}
ul.repositories+p.more{margin-top:20px;font-weight:bold;}
ul.repositories>li{list-style-type:none;margin:0 0 10px 0;padding:8px 10px 0 10px;border:1px solid #ddd;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;}
ul.repositories>li.public{background:url(/images/icons/public.png) 6px 9px no-repeat;}
ul.repositories>li.public.fork{background-image:url(/images/icons/public-fork.png);}
ul.repositories>li.private{background:url(/images/icons/private.png) 6px 9px no-repeat;border:1px solid #F7CA75;}
ul.repositories>li.private.fork{background:url(/images/icons/private-fork.png) 6px 9px no-repeat;}
ul.repositories>li.public.mirror{background-image:url(/images/icons/public-mirror.png);}
ul.repositories>li.simple{padding-bottom:8px;margin:0 0 3px 0;}
ul.repositories li.simple .body{display:none;}
ul.repositories .body{width:100%;margin-top:8px;margin-left:-10px;padding:5px 10px 5px 10px;border-top:1px solid #eee;background-color:#f1f1f1;background:#fafafa;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fafafa',endColorstr='#efefef');background:-webkit-gradient(linear,left top,left bottom,from(#fafafa),to(#efefef));background:-moz-linear-gradient(top,#fafafa,#efefef);-webkit-border-bottom-right-radius:4px;-webkit-border-bottom-left-radius:4px;-moz-border-radius-bottomright:4px;-moz-border-radius-bottomleft:4px;border-bottom-right-radius:4px;border-bottom-left-radius:4px;}
ul.repositories .private .body{background-color:#fffeeb;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#fffeeb',endColorstr='#fffee5');background:-webkit-gradient(linear,left top,left bottom,from(#fffeeb),to(#fffee5));background:-moz-linear-gradient(top,#fffeeb,#fffee5);}
ul.repositories ul.repo-stats{position:relative;float:right;border:none;font-size:11px;font-weight:bold;padding-left:15px;background:url(/images/modules/pagehead/actions_fade.png) 0 0 no-repeat;z-index:5;}
ul.repositories ul.repo-stats li{border:none;color:#666;}
ul.repositories ul.repo-stats li a{color:#666!important;border:none;background-color:transparent;background-position:5px -2px;}
ul.repositories h3{margin:0;padding-left:18px;font-size:14px;white-space:nowrap;}
ul.repositories li.simple h3{display:inline-block;}
ul.repositories .fork-flag{margin:0;padding-left:18px;font-size:11px;color:#777;white-space:nowrap;}
ul.repositories p.description{margin:0 0 3px 0;font-size:12px;color:#444;}
ul.repositories li.simple p.description{display:none;}
ul.repositories p.updated-at{margin:0;font-size:11px;color:#888;}
ul.repositories .graph{width:100%;padding:5px 4px;margin-top:5px;margin-left:-5px;text-align:center;background:#fff;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;border:1px solid #e5e5e5;border-right-color:#eee;border-bottom-color:#eee;}
ul.repositories .graph .bars{height:20px;}
.big-search{margin:5px 0 15px 0;padding-bottom:10px;border-bottom:1px solid #ddd;text-align:center;}
.big-search input.textfield{font-size:14px;padding:2px 5px;width:300px;}
.addon{margin:10px 0 10px -10px;width:100%;padding:5px;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.addon:hover{background:#e1eff8;}
.addon input[type=checkbox]{float:left;margin:5px 0 0 0;}
.addon h3{margin:0 0 2px 20px;font-size:16px;color:#222;}
.addon p{margin:0 0 0 20px;color:#444;}
.addon p+p{margin-top:1em;}
.addon.loading .indicator{display:inline-block;margin-left:5px;width:16px;height:16px;background:url(/images/modules/ajax/indicator.gif) 0 0 no-repeat;}
.addon.success .indicator{display:inline-block;margin-left:5px;width:16px;height:16px;background:url(/images/modules/ajax/success.png) 0 0 no-repeat;}
.addon.error .indicator{display:inline-block;margin-left:5px;width:16px;height:16px;background:url(/images/modules/ajax/error.png) 0 0 no-repeat;}
ul.hook-list{margin:0 0 15px 0;border-top:1px solid #ddd;}
ul.hook-list li{list-style-type:none;margin:0;padding:1px 0;font-size:12px;font-weight:bold;border-bottom:1px solid #ddd;}
ul.hook-list li a{display:block;padding:3px 0 3px 5px;color:#999;text-decoration:none;background:url(/images/modules/services/icons.png) 100% 0 no-repeat;}
ul.hook-list li.enabled a{color:#000;}
ul.hook-list li.enabled.inactive a{background-position:100% -100px;}
ul.hook-list li.active a{background-position:100% -50px;}
ul.hook-list li a.selected{color:#fff;background-color:#3d7cb9;}
.metabox{position:relative;margin-bottom:15px;font-size:12px;color:#333;padding:10px;background:#fafafa;border:1px solid #ddd;border-top:1px solid #fff;}
.metabox p{margin:0;}
.metabox p+p{margin-top:10px;}
.metabox em.placeholder{color:#666;}
.metabox .repository-homepage{margin-top:3px;}
.metabox .editable-text{width:100%;padding:1px 5px;margin-left:-5px;}
.metabox.pledgified .editable-text,.metabox.pledgified .inline-edit{width:700px;}
.metabox.pledgified .inline-edit{width:690px;}
.metabox .editable-text:hover{background:#fffcc3;}
.metabox em.edit-text{display:none;}
.metabox .editable-text:hover em.edit-text{display:inline;cursor:pointer;}
.metabox .rule{margin:10px 0;border-top:1px solid #ddd;border-bottom:1px solid #fff;clear:both;}
.metabox .editable-only{display:none;}
.metabox #repository_desc_wrapper{overflow:hidden;width:720px;}
.metabox #download_button,.metabox #download_button:visited{border:1px solid #d4d4d4;color:#666;display:block;float:right;font-size:15px;font-weight:bold;line-height:15px;margin-bottom:10px;padding:10px 15px 10px 16px;text-shadow:1px 1px 0 rgba(255,255,255,0.7);border-radius:5px;background:#ececec;background:-webkit-gradient(linear,center bottom,center top,from(#ececec),to(#f4f4f4));background:-moz-linear-gradient(90deg,#ececec,#f4f4f4);-moz-border-radius:5px;-moz-box-shadow:0 1px 0 #ececec;-webkit-box-shadow:0 1px 0 #ececec;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');}
.has-downloads-no-desc #download_button,.has-downloads-no-desc #download_button:visited{margin-bottom:0;}
.metabox #download_button .icon{background-image:url(/images/icons/download.png);background-position:0 52%;background-repeat:no-repeat;line-height:15px;margin:0 4px 0 0;padding:0 0 0 20px;}
.metabox #download_button:hover .icon,.metabox #download_button:active .icon{background-position:-21px 52%;}
.metabox #download_button:hover{border:1px solid #2e63a5;color:#fff;text-decoration:none;text-shadow:0 -1px 0 #2e63a5;background:#3570b8;background:-webkit-gradient(linear,center bottom,center top,from(#3570b8),to(#5e9ae2));background:-moz-linear-gradient(90deg,#3570b8,#5e9ae2);filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#3570b8',endColorstr='#5e9ae2');}
.metabox #download_button:active{border:1px solid #2e63a5;color:#fff;text-decoration:none;text-shadow:0 -1px 0 #2e63a5;background:-moz-linear-gradient(90deg,#558bcb,#336fb7);}
ul.clone-urls{margin:0;}
ul.clone-urls li{list-style-type:none;margin:5px 0 0 0;}
ul.clone-urls em{font-style:normal;color:#666;}
ul.clone-urls object{margin:0 0 -3px 3px;}
.url-box{height:23px;}
.has-downloads-no-desc .url-box{margin:9px 0;}
ul.clone-urls{float:left;margin:0;height:23px;}
ul.clone-urls li{list-style-type:none;float:left;margin:0;height:23px;padding:0;white-space:nowrap;border:none;overflow:visible;cursor:pointer;}
ul.clone-urls li.selected{border-right-color:#bbb;}
ul.clone-urls li:first-child a{-webkit-border-top-left-radius:3px;-webkit-border-bottom-left-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-bottomleft:3px;border-top-left-radius:3px;border-bottom-left-radius:3px;border-left:1px solid #d4d4d4;}
ul.clone-urls li>a{display:block;margin:0;height:21px;padding:0 9px 0 9px;font-size:11px;font-weight:bold;color:#333;text-shadow:1px 1px 0 #fff;text-decoration:none;line-height:21px;border:1px solid #d4d4d4;border-left:none;background:#f4f4f4;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#f4f4f4),to(#ececec));background:-moz-linear-gradient(top,#f4f4f4,#ececec);}
ul.clone-urls li>a:hover{color:#fff;text-decoration:none;text-shadow:-1px -1px 0 rgba(0,0,0,0.4);border-color:#518cc6;border-bottom-color:#2a65a0;background:#599bdc;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#599bdc',endColorstr='#3072b3');background:-webkit-gradient(linear,left top,left bottom,from(#599bdc),to(#3072b3));background:-moz-linear-gradient(top,#599bdc,#3072b3);}
ul.clone-urls li.selected>a{color:#000;text-shadow:1px 1px 0 rgba(255,255,255,0.6);border-color:#c9c9c9;border-bottom-color:#9a9a9a;background:#d7d7d7;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#d7d7d7',endColorstr='#ababab');background:-webkit-gradient(linear,left top,left bottom,from(#d7d7d7),to(#ababab));background:-moz-linear-gradient(top,#d7d7d7,#ababab);}
input.url-field{float:left;width:330px;padding:3px 5px 2px 5px;height:16px;border:1px solid #ccc;border-left:none;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:11px;color:#666;}
.url-box p{float:left;margin:0 0 0 5px;height:23px;line-height:23px;font-size:11px;color:#666;}
.url-box p strong{color:#000;}
.url-box .clippy-tooltip{float:left;margin:4px 0 0 5px;}
.pledgie{float:right;margin:0 0 10px 20px;}
.adminmetabox .pledgie{margin-bottom:0;}
a.pledgie-button{height:30px;padding:0 0 0 65px;font-size:12px;font-weight:bold;color:#333;text-decoration:none;text-shadow:1px 1px 0 #fff;background:url(/images/modules/pagehead/pledgie_button.gif) 0 0 no-repeat;}
a.pledgie-button span{position:relative;right:-2px;display:block;height:30px;line-height:30px;padding-right:10px;background:url(/images/modules/pagehead/pledgie_button.gif) 100% 0 no-repeat;}
a.pledgie-button:hover{color:#000;background-position:0 -30px;}
a.pledgie-button:hover span{background-position:100% -30px;}
a.edit-pledgie{display:block;margin-top:5px;text-align:center;font-size:11px;font-weight:bold;}
ul.repo-stats{display:inline-block;*display:inline;margin:0;border:1px solid #ddd;-webkit-border-radius:3px;-moz-border-radius:3px;background:#fff;}
ul.repo-stats li{list-style-type:none;display:inline-block;margin:0!important;}
ul.repo-stats li a{display:inline-block;height:21px;padding:0 5px 0 23px;line-height:21px;color:#666;border-left:1px solid #ddd;background-repeat:no-repeat;background-position:5px -2px;}
ul.repo-stats li:first-child a{border-left:none;margin-right:-3px;}
ul.repo-stats li a:hover{color:#fff!important;background:#4183c4;text-decoration:none;background-repeat:no-repeat;background-position:5px -27px;}
ul.repo-stats li:first-child a:hover{-webkit-border-top-left-radius:3px;-webkit-border-bottom-left-radius:3px;-moz-border-radius-topleft:3px;-moz-border-radius-bottomleft:3px;}
ul.repo-stats li:last-child a:hover{-webkit-border-top-right-radius:3px;-webkit-border-bottom-right-radius:3px;-moz-border-radius-topright:3px;-moz-border-radius-bottomright:3px;}
ul.repo-stats li.watchers a{background-image:url(/images/modules/pagehead/repostat_watchers.png);}
ul.repo-stats li.watchers.watching a{background-image:url(/images/modules/pagehead/repostat_watchers-watching.png);color:#333;}
ul.repo-stats li.forks a{background-image:url(/images/modules/pagehead/repostat_forks.png);}
ul.repo-stats li.forks.forked a{background-image:url(/images/modules/pagehead/repostat_forks-forked.png);color:#333;}
ul.repo-stats li.collaborators a{background-image:url(/images/icons/collab.png);background-position:3px 3px!important;color:#333;margin-left:8px;}
.highlight .gc{color:#999;background-color:#EAF2F5;}
#footer{margin:25px 0 0 0;padding:20px 0 15px 0;font-size:12px;border-top:2px solid #ddd;background:#f1f1f1;}
#footer p.company{margin:0;font-weight:bold;}
#footer ul.links{margin:0 0 5px 0;height:16px;}
#footer ul.links li{list-style-type:none;float:left;margin:0 10px 0 0;}
#footer ul.links li.blog{font-weight:bold;}
#footer ul.sosueme{margin:0 0 5px 0;height:16px;}
#footer ul.sosueme li{list-style-type:none;float:left;margin:0 10px 0 0;}
#footer ul.sosueme li.main{font-weight:bold;color:#000;}
#footer ul.sosueme li a{color:#666;}
#footer .sponsor{float:right;white-space:nowrap;color:#777;line-height:1.6;}
#footer .sponsor a{color:#333;}
#footer .sponsor .logo{float:left;margin-right:10px;}
#errornew{margin-top:2em;text-align:center;}
#errornew.standard h1{font-size:140%;margin-top:1em;}
#errornew.standard p{margin:.75em 0;font-weight:bold;}
#errornew.standard ul{margin:.75em 0;list-style-type:none;}
#error{margin-top:2em;text-align:center;}
#error h1{font-size:140%;margin-top:1em;}
#error ul{padding-left:1em;}
#error .status500,#error .status404{width:36em;margin:10px auto;text-align:left;}
#error .status500 p,#error .status404 p{font-weight:bold;margin:10px 0;}
#error .maintenance{text-align:center;}
#error .maintenance p{text-align:center;font-weight:bold;}
.standard_form{margin:3em auto 0 auto;background-color:#eaf2f5;padding:2em 2em 1em 2em;border:20px solid #ddd;}
.standard_form .nothing-to-see-here{font-size:18px;font-weight:bold;color:#222;margin-top:0;}
.standard_form pre{font-size:13px;}
.standard_form h1{font-size:160%;margin-bottom:1em;}
.standard_form h1 a{font-size:70%;font-weight:normal;}
.standard_form h2{margin:0;}
.standard_form p{margin:.5em 0;}
.standard_form p.note{color:#a00;}
.standard_form form label,.standard_form form .label,label.standard{font-size:110%;color:#666;display:block;margin:0;margin-top:1em;}
.standard_form form label a{font-size:90%;}
.standard_form form label.error{color:#a00;}
.standard_form form .label label{margin:0;color:black;font-size:95%;}
.standard_form form .label span{font-size:90%;color:#888;}
.standard_form form input.text,.standard_form form textarea{padding:5px;border:1px solid #888;}
.standard_form form input.text{font-size:110%;}
.standard_form form input.submit{font-size:120%;padding:.1em 1em;}
input[type=text].error,.standard_form form label.error input.text,.standard_form form label.error textarea{border:1px solid #a00;background-color:#f2e1e1;}
.login_form{margin:5em auto;}
.login_form .formbody{padding:2em;background-color:#e9f1f4;overflow:hidden;border-style:solid;border-width:1px 1px 2px;border-color:#e9f1f4 #d8dee2 #d8dee2;border-radius:0 0 3px 3px;-moz-border-radius:0 0 3px 3px;-webkit-border-radius:0 0 3px 3px;}
.login_form .nothing-to-see-here{font-size:18px;font-weight:bold;color:#222;margin-top:0;}
.login_form pre{font-size:13px;}
.login_form h1{color:#fff;font-size:16px;font-weight:bold;background-color:#405a6a;background:-moz-linear-gradient(center top,'#829AA8','#405A6A');filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#829aa8',endColorstr='#405a6a');background:-webkit-gradient(linear,left top,left bottom,from(#829aa8),to(#405a6a));background:-moz-linear-gradient(top,#829aa8,#405a6a);border:1px solid #677c89;border-bottom-color:#6b808d;border-radius:3px 3px 0 0;-moz-border-radius:3px 3px 0 0;-webkit-border-radius:3px 3px 0 0;text-shadow:0 -1px 0 rgba(0,0,0,0.7);margin:0;padding:8px 18px;}
.login_form h1 a{font-size:70%;font-weight:normal;color:#E9F1F4;text-shadow:none;}
.login_form p{color:#2f424e;font-size:12px;font-weight:normal;margin:0;text-shadow:0 -1px 0 rgba(100,100,100,0.1);}
.login_form p.note{color:#a00;}
.login_form ul{border-bottom:1px solid #d8dee2;padding:0 0 2em 0;margin:.2em 0 1.5em 0;}
.login_form ul li{list-style-position:inside;font-weight:bold;color:#2f424e;font-size:12px;}
.login_form form label,.login_form form .label,label.standard{font-size:110%;color:#2f424e;text-shadow:0 -1px 0 rgba(100,100,100,0.1);display:inline-block;cursor:text;}
.login_form form label a{font-size:90%;}
.login_form form label.error{color:#a00;}
.login_form form .label label{margin:0;color:black;font-size:95%;}
.login_form form .label span{font-size:90%;color:#888;}
.login_form form input.text,.login_form form textarea{padding:5px;border:1px solid #d8dee2;margin:.2em 0 1em 0;}
.login_form form input.text{font-size:110%;}
.login_form button{margin:0 8px 0 0;}
.login_form form input[type=submit]{display:inline-block;height:34px;padding:0;position:relative;top:1px;margin-left:10px;font-family:helvetica,arial,freesans,clean,sans-serif;font-weight:bold;font-size:12px;color:#333;text-shadow:1px 1px 0 #fff;white-space:nowrap;border:none;overflow:visible;background:#ddd;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#ffffff',endColorstr='#e1e1e1');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fff),to(#e1e1e1));background:-moz-linear-gradient(-90deg,#fff,#e1e1e1);border-bottom:1px solid #ebebeb;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;-webkit-box-shadow:0 1px 4px rgba(0,0,0,0.3);-moz-box-shadow:0 1px 4px rgba(0,0,0,0.3);box-shadow:0 1px 4px rgba(0,0,0,0.3);cursor:pointer;margin-left:1px;padding:0 13px;-webkit-font-smoothing:subpixel-antialiased!important;}
.login_form form input[type=submit]:hover{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);border-bottom-color:#0770a0;background:#0770a0;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#0ca6dd',endColorstr='#0770a0');background:-webkit-gradient(linear,0% 0,0% 100%,from(#0ca6dd),to(#0770a0));background:-moz-linear-gradient(-90deg,#0ca6dd,#0770a0);}
.login_form form .error_box,.login_form form .notification{margin-bottom:1em;}
input[type=text].error,.login_form form label.error input.text,.login_form form label.error textarea{border:1px solid #a00;background-color:#f2e1e1;}
.login_form form p.hint{margin:-1em 0 1em 0;color:gray;}
.forgot_password_form{margin:5em auto;}
.forgot_password_form .formbody{padding:2em;background-color:#e9f1f4;overflow:hidden;border-style:solid;border-width:1px 1px 2px;border-color:#e9f1f4 #d8dee2 #d8dee2;border-radius:0 0 3px 3px;-moz-border-radius:0 0 3px 3px;-webkit-border-radius:0 0 3px 3px;}
.forgot_password_form .nothing-to-see-here{font-size:18px;font-weight:bold;color:#222;margin-top:0;}
.forgot_password_form pre{font-size:13px;}
.forgot_password_form h1{color:#fff;font-size:16px;font-weight:bold;background-color:#405a6a;background:-moz-linear-gradient(center top,'#829AA8','#405A6A');filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#829aa8',endColorstr='#405a6a');background:-webkit-gradient(linear,left top,left bottom,from(#829aa8),to(#405a6a));background:-moz-linear-gradient(top,#829aa8,#405a6a);border:1px solid #677c89;border-bottom-color:#6b808d;border-radius:3px 3px 0 0;-moz-border-radius:3px 3px 0 0;-webkit-border-radius:3px 3px 0 0;text-shadow:0 -1px 0 rgba(0,0,0,0.7);margin:0;padding:8px 18px;}
.forgot_password_form h1 a{font-size:70%;font-weight:normal;color:#E9F1F4;text-shadow:none;}
.forgot_password_form p{color:#2f424e;font-size:12px;font-weight:normal;margin:0;text-shadow:0 -1px 0 rgba(100,100,100,0.1);}
.forgot_password_form p.note{color:#a00;}
.forgot_password_form ul{border-bottom:1px solid #d8dee2;padding:0 0 2em 0;margin:.2em 0 1.5em 0;}
.forgot_password_form ul li{list-style-position:inside;font-weight:bold;color:#2f424e;font-size:12px;}
.forgot_password_form form label,.forgot_password_form form .label,label.standard{font-size:110%;color:#2f424e;text-shadow:0 -1px 0 rgba(100,100,100,0.1);display:inline-block;cursor:text;}
.forgot_password_form form label a{font-size:90%;}
.forgot_password_form form label.error{color:#a00;}
.forgot_password_form form .label label{margin:0;color:black;font-size:95%;}
.forgot_password_form form .label span{font-size:90%;color:#888;}
.forgot_password_form form input.text,.forgot_password_form form textarea{padding:5px;border:1px solid #d8dee2;margin:.2em 0 1em 0;}
.forgot_password_form form input.text{font-size:110%;}
.forgot_password_form button{margin:0 8px 0 0;}
.forgot_password_form form input[type=submit]{display:inline-block;height:34px;padding:0;position:relative;top:1px;margin-left:10px;font-family:helvetica,arial,freesans,clean,sans-serif;font-weight:bold;font-size:12px;color:#333;text-shadow:1px 1px 0 #fff;white-space:nowrap;border:none;overflow:visible;background:#ddd;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#ffffff',endColorstr='#e1e1e1');background:-webkit-gradient(linear,0% 0,0% 100%,from(#fff),to(#e1e1e1));background:-moz-linear-gradient(-90deg,#fff,#e1e1e1);border-bottom:1px solid #ebebeb;-webkit-border-radius:4px;-moz-border-radius:4px;border-radius:4px;-webkit-box-shadow:0 1px 4px rgba(0,0,0,0.3);-moz-box-shadow:0 1px 4px rgba(0,0,0,0.3);box-shadow:0 1px 4px rgba(0,0,0,0.3);cursor:pointer;margin-left:1px;padding:0 13px;-webkit-font-smoothing:subpixel-antialiased!important;}
.forgot_password_form form input[type=submit]:hover{color:#fff;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);border-bottom-color:#0770a0;background:#0770a0;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#0ca6dd',endColorstr='#0770a0');background:-webkit-gradient(linear,0% 0,0% 100%,from(#0ca6dd),to(#0770a0));background:-moz-linear-gradient(-90deg,#0ca6dd,#0770a0);}
.forgot_password_form form .error_box,.forgot_password_form form .notification{margin-bottom:1em;}
input[type=text].error,.forgot_password_form form label.error input.text,.forgot_password_form form label.error textarea{border:1px solid #a00;background-color:#f2e1e1;}
.oauth_form{margin:5em auto;}
.oauth_form .formbody{padding:2em;background-color:#e9f1f4;overflow:hidden;border-style:solid;border-width:1px 1px 2px;border-color:#e9f1f4 #d8dee2 #d8dee2;border-radius:0 0 3px 3px;-moz-border-radius:0 0 3px 3px;-webkit-border-radius:0 0 3px 3px;}
.oauth_form .nothing-to-see-here{font-size:18px;font-weight:bold;color:#222;margin-top:0;}
.oauth_form pre{font-size:13px;}
.oauth_form h1{color:#fff;font-size:16px;font-weight:bold;background-color:#405a6a;background:-moz-linear-gradient(center top,'#829AA8','#405A6A');filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#829aa8',endColorstr='#405a6a');background:-webkit-gradient(linear,left top,left bottom,from(#829aa8),to(#405a6a));background:-moz-linear-gradient(top,#829aa8,#405a6a);border:1px solid #677c89;border-bottom-color:#6b808d;border-radius:3px 3px 0 0;-moz-border-radius:3px 3px 0 0;-webkit-border-radius:3px 3px 0 0;text-shadow:0 -1px 0 rgba(0,0,0,0.7);margin:0;padding:8px 18px;}
.oauth_form h1 a{font-size:70%;font-weight:normal;}
.oauth_form h2{color:#2f424e;font-size:18px;font-weight:normal;margin:0 0 .5em;text-shadow:0 -1px 0 rgba(100,100,100,0.1);}
.oauth_form p{color:#2f424e;font-size:12px;font-weight:normal;margin:0;text-shadow:0 -1px 0 rgba(100,100,100,0.1);}
.oauth_form p.note{color:#a00;}
.oauth_form ul{border-bottom:1px solid #d8dee2;padding:0 0 2em 0;margin:.2em 0 1.5em 0;}
.oauth_form ul li{list-style-position:inside;font-weight:bold;color:#2f424e;font-size:12px;}
.oauth_form form label,.oauth_form form .label,label.standard{font-size:110%;color:#666;display:block;margin:0;margin-top:1em;}
.oauth_form form label a{font-size:90%;}
.oauth_form form label.error{color:#a00;}
.oauth_form form .label label{margin:0;color:black;font-size:95%;}
.oauth_form form .label span{font-size:90%;color:#888;}
.oauth_form form input.text,.oauth_form form textarea{padding:5px;border:1px solid #888;}
.oauth_form form input.text{font-size:110%;}
.oauth_form button{margin:0 8px 0 0;}
.oauth_form form input.submit{font-size:120%;padding:.1em 1em;}
input[type=text].error,.oauth_form form label.error input.text,.oauth_form form label.error textarea{border:1px solid #a00;background-color:#f2e1e1;}
#contact-form{margin-top:1.3em;}
#contact-form td{padding:.5em;}
#contact-form input[type='text'],#contact-form textarea{width:30em;}
.page_form th,.page_form td{padding:5px;}
.page_form th{padding-right:10px;text-align:right;}
.page_form td textarea{width:400px;height:70px;}
#profile{margin:3em auto 0 auto;width:60em;}
#login{width:31em;}
#forgot_password{width:31em;}
#testimonials{text-align:center;padding-top:2em;}
#testimonials .quotes{margin-left:2em;}
#testimonials blockquote{margin:2em auto;font-style:italic;color:#666;width:15em;float:left;margin-right:1em;min-height:8.5em;}
#testimonials blockquote span{text-align:right;display:block;}
#commit{overflow:hidden;}
#commit h2{margin:0;}
#commit .group{border-top:1px solid #bedce7;}
#commit .separator{padding-top:1em;}
#commit .envelope{border-bottom:1px solid #bedce7;border-left:1px solid #bedce7;border-right:1px solid #bedce7;padding:0 .7em .7em .7em;background:#eaf2f5 url(/images/modules/commit/bg_gradient.gif) 0 100% repeat-x;overflow:hidden;}
#commit .envelope.selected{background:#fffeeb!important;}
#commit .envelope.selected .machine span{border-bottom:1px dotted #4183c4;}
#commit.single_commit .envelope .machine span{border-bottom:1px dotted #4183c4;}
#commit .human{padding-top:.7em;float:left;width:50em;}
#commit .human .refs{font-size:150%;}
#commit .human .message{font-size:80%;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;}
#commit .human .message pre{white-space:pre-wrap;word-wrap:break-word;width:48em;}
#commit .human .message a{color:#000;}
#commit .human .message a.vis{color:#4183c4;}
#commit .human .actor{clear:left;margin-top:.75em;}
#commit .human .actor .gravatar{border:1px solid #d0d0d0;padding:2px;background-color:white;float:left;line-height:0;margin-right:.7em;}
#commit .human .actor .name{line-height:1.5em;}
#commit .human .actor .name a{color:#000;}
#commit .human .actor .name span{color:#888;font-size:90%;}
#commit .human .actor .date{color:#888;font-size:90%;line-height:1em;}
#commit .merge{padding-top:.7em;}
#commit .merge a{color:#000;}
#commit .merge .gravatar{border:1px solid #d0d0d0;padding:2px;background-color:white;float:left;margin-right:.5em;}
#commit .merge .message{margin-top:.2em;}
#commit .machine{float:right;width:18em;padding:.8em 0 .8em 1.2em;border-left:1px solid #bedce7;color:#808080;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:.85em;line-height:1.5em;}
#commit .commit_oneline{background:#eaf2f5 url(/images/modules/commit/bg_gradient.gif) 0 100% repeat-x;}
#commit .commit_oneline td{border-bottom:1px solid #bedce7;}
#commit .commit_oneline .date{color:#888;width:1%;padding:0 1em 0 .5em;border-left:1px solid #bedce7;}
#commit .commit_oneline .author{width:15%;}
#commit .commit_oneline .gravatar{width:1%;}
#commit .commit_oneline .gravatar img{border:1px solid #d0d0d0;padding:1px;background-color:white;float:left;margin-right:.4em;}
#commit .commit_oneline .author a{font-weight:bold;color:black;}
#commit .commit_oneline .message{font-size:75%;}
#commit .commit_oneline .message a{color:black;}
#commit .commit_oneline .commit,#commit .commit_oneline .tree{width:1%;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:90%;color:#808080;border-left:1px solid #bedce7;padding:.6em .5em;}
#commit .commit_oneline .tree{border-right:1px solid #bedce7;}
#all_commit_comments .comment .body img{max-width:67.5em;}
#path,.breadcrumb{font-size:140%;padding:.8em 0;}
#toc{font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:90%;}
table#toc{border-top:1px solid #ddd;border-spacing:0;padding:0;margin:10px 0;width:100%;}
#toc td{padding:.4em 5px .4em 5px;border-bottom:1px solid #ddd;}
#toc td.status{width:20px;padding-left:0;}
#toc td.status .stat-icon{display:block;width:20px;height:19px;text-indent:-9999px;background:url(/images/modules/commit/file_modes.png) 0 0 no-repeat;}
#toc td.modified .stat-icon{background-position:0 -50px;}
#toc td.added .stat-icon{background-position:0 0;}
#toc td.removed .stat-icon{background-position:0 -100px;}
#toc td.renamed .stat-icon{background-position:0 -150px;}
#toc .diffstat{padding-right:0;width:1%;}
#toc .diffstat{white-space:nowrap;text-align:right;}
#toc .diffstat a{text-decoration:none;padding-right:15px;background:url(/images/modules/commit/jump.png) 100% 5px no-repeat;}
#toc .diffstat a:hover{background-position:100% -45px;}
#toc .diffstat-summary{font-family:helvetica,arial,freesans,clean,sans-serif;text-align:right;color:#666;font-weight:bold;font-size:11px;}
#toc .diffstat-bar{display:inline-block;width:50px;height:9px;text-decoration:none;text-align:left;background:url(/images/modules/commit/diffstat.png) 0 -100px repeat-x;}
#toc .diffstat .plus{float:left;display:block;width:10px;height:9px;text-indent:-9999px;background:url(/images/modules/commit/diffstat.png) 0 0 repeat-x;}
#toc .diffstat .minus{float:left;width:10px;height:9px;text-indent:-9999px;background:url(/images/modules/commit/diffstat.png) 0 -50px repeat-x;}
#entice{background-color:#f0fff0;border:1px solid #accbac;display:block;margin:2px 0 15px;overflow:hidden;padding:20px;border-radius:5px;-moz-border-radius:5px;-webkit-border-radius:5px;-moz-box-shadow:0 1px 3px #ddd;-webkit-box-shadow:0 1px 3px #ddd;}
#entice h2{color:#333;font-size:20px;font-weight:normal;line-height:normal;margin:0;padding:0;text-shadow:0 1px 0 #fff;}
#entice h2 strong{line-height:normal;}
#entice .explanation{float:left;width:550px;}
#entice .explanation p{margin-bottom:0;text-shadow:0 1px 0 #fff;}
#entice .signup{float:right;}
#entice .signup #entice-signup-button,#entice .signup #entice-signup-button:visited{border:1px solid #3e9533;border-bottom-color:#3e9533;color:#fff;display:block;font-size:20px;font-weight:bold;line-height:15px;margin:0 0 8px;padding:26px 30px 24px;text-decoration:none;text-shadow:-1px -1px 0 rgba(0,0,0,0.3);border-radius:5px;-moz-border-radius:5px;-moz-box-shadow:0 0 1px #ddd;-webkit-box-shadow:0 0 1px #ddd;background:#3e9533;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#419b36',endColorstr='#357f2c');background:-webkit-gradient(linear,0% 0,0% 100%,from(#419b36),to(#357f2c));background:-moz-linear-gradient(-90deg,#419b36,#357f2c);border-bottom-color:#3e9533;}
#entice .signup #entice-signup-button:hover{border:1px solid #2e63a5;color:#fff;text-decoration:none;text-shadow:0 -1px 0 #2e63a5;background:#3570b8;background:-webkit-gradient(linear,center bottom,center top,from(#3570b8),to(#5e9ae2));background:-moz-linear-gradient(90deg,#3570b8,#5e9ae2);filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#3570b8',endColorstr='#5e9ae2');}
#entice #oss-caption{color:#666;font-size:10px;font-weight:bold;line-height:normal;margin:0;padding:0;text-align:center;text-shadow:0 1px 0 #fff;text-transform:uppercase;}
.tree-browser{border-top:1px solid #d8d8d8;border-left:1px solid #d8d8d8;border-right:1px solid #d8d8d8;width:920px;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:90%;margin:0;margin-bottom:1em;}
.tree-browser th{text-align:left;font-weight:normal;background-color:#eaeaea;color:#999;padding:.5em .3em;border-bottom:1px solid #d8d8d8;}
.tree-browser .history{float:right;padding-right:5px;}
.tree-browser td{background:#f8f8f8 url(/images/modules/browser/row_bg.png) 0 100% repeat-x;padding:.5em .3em;color:#484848;border-bottom:1px solid #e1e1e1;}
.tree-browser tr.current td{background:none;background-color:#fffeeb;}
.tree-browser td.icon{width:1.3em;}
.tree-browser td a.message{color:#484848;}
.tree-browser td span.ref{color:#aaa;}
.tree-browser.downloads td{vertical-align:top;}
.tree-browser.downloads td p{margin:0;padding:0;}
#files .file,.file-box{border:1px solid #ccc;margin-bottom:1em;}
#files .file .highlight,.file-box .highlight{border:none;padding:0;}
#files .file .meta,.file-box .meta{padding:0 5px;height:33px;line-height:33px;font-size:12px;color:#333;background:url(/images/modules/commit/file_head.gif) 0 0 repeat-x #eee;text-shadow:1px 1px 0 rgba(255,255,255,0.5);border-bottom:1px solid #ccc;overflow:hidden;}
#files .file .meta .info,.file-box .meta .info{float:left;height:33px;line-height:33px;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;}
#files .file .meta .info span,.file-box .meta .info span{padding-left:9px;margin-left:5px;background:url(/images/modules/commit/action_separator.png) 0 50% no-repeat;}
#files .file .meta .info span:first-child,#files .file .meta .info .icon+span,.file-box .meta .info span:first-child,.file-box .meta .info .icon+span{background:transparent;margin-left:0;padding-left:0;}
#files .file .meta .info span.icon,.file-box .meta .info span.icon{line-height:0;float:left;margin:5px 5px 0 0;padding:3px;background:#f7f7f7;border:1px solid #ccc;border-right-color:#e5e5e5;border-bottom-color:#e5e5e5;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
#files .file .meta .actions,.file-box .meta .actions{float:right;height:33px;line-height:33px;}
#files .file .meta .actions li,.file-box .meta .actions li{list-style-type:none;float:left;margin:0 0 0 7px;height:33px;line-height:33px;padding-left:9px;font-size:11px;background:url(/images/modules/commit/action_separator.png) 0 50% no-repeat;}
#files .file .meta .actions li:first-child,.file-box .meta .actions li:first-child{background:transparent;margin-left:0;padding-left:0;}
#files .file .meta .actions li a,.file-box .meta .actions li a{font-weight:bold;}
#files .file .meta .actions li code,.file-box .meta .actions li code{font-size:11px;}
#files .file .meta .actions li label input,.file-box .meta .actions li label input{position:relative;top:1px;}
#files .file .data,.file-box .data{font-size:80%;overflow:auto;background-color:#f8f8ff;}
#files .file .data.empty,.file-box .data.empty{font-size:90%;padding:5px 10px;color:#777;}
#files .file .data pre,#files .file .line-data,#files .file .line-number,.file-box .data pre,.file-box .line-data,.file-box .line-number{font-family:'Bitstream Vera Sans Mono','Courier',monospace;font-size:12px;}
#files .file .data .highlight,.file-box .data .highlight{padding:1em 0;}
#files .file .data .highlight div,.file-box .data .highlight div{padding-left:1em;}
#files .file .data .line_numbers,.file-box .data .line_numbers{background-color:#ececec;color:#aaa;padding:1em .5em;border-right:1px solid #ddd;text-align:right;}
#files .file .data td.line_numbers,.file-box .data td.line_numbers{padding:0 .5em;font-family:'Bitstream Vera Sans Mono','Courier',monospace;font-size:12px;-moz-user-select:none;-khtml-user-select:none;user-select:none;}
.windows #files .file .data pre,.windows #files .file .line-data,.windows #files .file .line-number,.linux #files .file .data pre,.linux #files .file .line-data,.linux #files .file .line-number,.windows .file-box .data pre,.windows .file-box .line-data,.windows .file-box .line-number,.linux .file-box .data pre,.linux .file-box .line-data,.linux .file-box .line-number,.windows #files .file .data td.line_numbers,.linux #files .file .data td.line_numbers,.windows .file-box .data td.line_numbers,.linux .file-box .data td.line_numbers{font-family:'Bitstream Vera Sans Mono','Courier New',monospace;}
td.linkable-line-number{cursor:pointer;}
td.linkable-line-number:hover{text-decoration:underline;}
#files .file .data .line_numbers span,.file-box .data .line_numbers span{color:#aaa;cursor:pointer;}
#files .image,.file-box .image{text-align:center;background-color:#ddd;padding:30px;position:relative;}
#files .file .glif,.file-box .glif{background-color:#f0f0f0;border-bottom:1px solid #dedede;padding:.5em 0;}
#files .file .glif table,#files .file .image table,.file-box .glif table,.file-box .image table{margin:0 auto;}
#files .file .glif table td,#files .file .image table td,.file-box .glif table td,.file-box .image table td{font-size:70%;text-align:center;color:#888;}
#files .file .image .added-frame,.file-box .image .added-frame,#files .file .image .deleted-frame,.file-box .image .deleted-frame{border:1px solid #ddd;display:inline-block;line-height:0;position:relative;}
#files .file .image .border-wrap,.file-box .image .border-wrap{background-color:white;border:1px solid #999;display:inline-block;line-height:0;position:relative;}
#files .file .image .deleted-frame,.file-box .image .deleted-frame{background-color:white;border:1px solid #f77;}
#files .file .image .added-frame,.file-box .image .added-frame{border:1px solid #63c363;}
#files .file .image a,.file-box .image a{display:inline-block;line-height:0;}
#files .file .glif table canvas,.file-box .glif table canvas{border:1px solid #ddd;background-color:white;}
#files .file .image table td,.file-box .image table td{vertical-align:top;padding:0 5px;}
#files .file .image table td img,.file-box .image table td img{max-width:100%;}
#files .file .image img,.file-box .image img,#files .file .image canvas,.file-box .image canvas{background:url(/images/modules/commit/trans_bg.gif) right bottom #eee;max-width:600px;border:1px solid #fff;}
#files .file .image .view img,.file-box .image .view img,#files .file .image .view canvas,.file-box .image .view canvas{background:url(/images/modules/commit/trans_bg.gif) right bottom #eee;position:relative;top:0;right:0;max-width:inherit;}
#files .file .view-modes,.file-box .view-modes{font-size:12px;color:#333;background:url(/images/modules/commit/file_head.gif) 0 0 repeat-x #eee;text-shadow:1px 1px 0 rgba(255,255,255,0.5);overflow:hidden;text-align:center;}
#files .file .view-modes ul.menu,.file-box .view-modes ul.menu{display:inline-block;list-style-type:none;background-repeat:no-repeat;height:33px;position:relative;}
#files .file .view-modes ul.menu li,.file-box .view-modes ul.menu li{display:inline-block;background:url(/images/modules/commit/action_separator.png) 0 50% no-repeat;padding:0 0 0 12px;margin:0 10px 0 0;color:#777;cursor:pointer;height:33px;line-height:33px;}
#files .file .hidden,.file-box .hidden{display:none!important;}
#files .file .view-modes ul.menu li:first-child,.file-box .view-modes ul.menu li:first-child{background:none;}
#files .file .view-modes ul.menu li.active,.file-box .view-modes ul.menu li.active{color:#333;cursor:default;}
#files .file .view-modes ul.menu li.disabled:hover,.file-box .view-modes ul.menu li.disabled:hover{text-decoration:none;}
#files .file .view-modes ul.menu li.disabled,.file-box .view-modes ul.menu li.disabled{color:#ccc;cursor:default;}
#files .file .view-modes ul.menu li:hover,.file-box .view-modes ul.menu li:hover{text-decoration:underline;}
#files .file .view-modes ul.menu li.active:hover,.file-box .view-modes ul.menu li.active:hover{text-decoration:none;}
#files .bubble,.file-box .bubble{background:url(/images/modules/commit/off_comment_bubble.png) no-repeat;color:white;height:1.4em;margin:-0.2em 0 0 -9.6em;padding:.1em .8em 0 0;padding-left:0!important;position:absolute;width:1.5em;cursor:pointer;}
.uncommentable #files .bubble{display:none;}
#files .bubble.commented,.file-box .bubble.commented{background:url(/images/modules/commit/comment_bubble.png) no-repeat;}
#files .meta .bubble,.file-box .meta .bubble{font-family:'Bitstream Vera Sans Mono','Courier',monospace;margin:-0.2em 0 0 -3.9em;height:1.5em;}
#files .empty,.file-box .empty{background:none;}
#files .bubble span,.file-box .bubble span{display:block;line-height:1.4em;text-align:center;}
#files .progress,.file-box .progress{margin:30px;z-index:101;position:relative;}
#files .progress h3,.file-box .progress h3{color:#555;}
#files .progress .progress-frame,.file-box .progress .progress-frame{display:block;height:15px;width:300px;background-color:#eee;border:1px solid #ccc;margin:0 auto;-webkit-border-radius:10px;-moz-border-radius:10px;border-radius:10px;overflow:hidden;}
#files .progress .progress-bar,.file-box .progress .progress-bar{display:block;height:15px;width:5%;background-color:#f00;-webkit-border-radius:10px;-moz-border-radius:10px;border-radius:10px;background:#4183C4;background:-moz-linear-gradient(top,#7db9e8 0,#4183C4 100%);background:-webkit-gradient(linear,left top,left bottom,color-stop(0%,#7db9e8),color-stop(100%,#4183C4));filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#7db9e8',endColorstr='#4183C4',GradientType=0);}
#files .image .d-red{color:#F77;}
#files .image .a-green{color:#63c363;}
#files .image .view>span,.file-box .image .view>span{vertical-align:middle;}
#files .image .two-up,.file-box .image .two-up{display:block;letter-spacing:16px;}
#files .image .two-up .shell,.file-box .image .two-up .shell{display:inline-block;line-height:0;}
#files .image .two-up .shell p,.file-box .image .two-up .shell p{letter-spacing:normal;font-size:.8em;color:#999;}
#files .image .two-up .deleted,.file-box .image .two-up .deleted{display:inline-block;}
#files .image .two-up .added,.file-box .image .two-up .added{display:inline-block;}
#files .image .swipe .swipe-frame,.file-box .image .swipe .swipe-frame,#files .image .onion-skin .onion-skin-frame,.file-box .image .onion-skin .onion-skin-frame{display:block;margin:auto;position:relative;}
#files .image .swipe .deleted-frame,.file-box .image .swipe .deleted-frame,#files .image .swipe .swipe-shell,.file-box .image .swipe .swipe-shell{position:absolute;display:block;top:13px;right:7px;}
#files .image .swipe .swipe-shell,.file-box .image .swipe .swipe-shell{overflow:hidden;border-left:1px solid #999;}
#files .image .swipe .added-frame,.file-box .image .swipe .added-frame{display:block;position:absolute;top:0;right:0;}
#files .image .swipe .swipe-bar,.file-box .image .swipe .swipe-bar{display:block;height:100%;width:15px;z-index:100;position:absolute;cursor:pointer;}
#files .image .swipe .top-handle,.file-box .image .swipe .top-handle{display:block;height:14px;width:15px;position:absolute;top:0;background:url(/images/modules/commit/swipemode_sprites.gif) 0 3px no-repeat;}
#files .image .swipe .bottom-handle,.file-box .image .swipe .bottom-handle{display:block;height:14px;width:15px;position:absolute;bottom:0;background:url(/images/modules/commit/swipemode_sprites.gif) 0 -11px no-repeat;}
#files .image .swipe .swipe-bar:hover .top-handle,.file-box .image .swipe .swipe-bar:hover .top-handle{background-position:-15px 3px;}
#files .image .swipe .swipe-bar:hover .bottom-handle,.file-box .image .swipe .swipe-bar:hover .bottom-handle{background-position:-15px -11px;}
#files .image .onion-skin .deleted-frame,.file-box .image .onion-skin .deleted-frame,#files .image .onion-skin .added-frame,.file-box .image .onion-skin .added-frame{position:absolute;display:block;top:0;left:0;}
#files .image .onion-skin .controls,.file-box .image .onion-skin .controls{display:block;height:14px;width:300px;z-index:100;position:absolute;bottom:0;left:50%;margin-left:-150px;}
#files .image .onion-skin .controls .transparent,.file-box .image .onion-skin .controls .transparent{display:block;position:absolute;top:2px;right:0;height:10px;width:10px;background:url(/images/modules/commit/onion_skin_sprites.gif) -2px -0px no-repeat;}
#files .image .onion-skin .controls .opaque,.file-box .image .onion-skin .controls .opaque{display:block;position:absolute;top:2px;left:0;height:10px;width:10px;background:url(/images/modules/commit/onion_skin_sprites.gif) -2px -10px no-repeat;}
#files .image .onion-skin .controls .drag-track,.file-box .image .onion-skin .controls .drag-track{display:block;position:absolute;left:12px;height:10px;width:276px;background:url(/images/modules/commit/onion_skin_sprites.gif) -4px -20px repeat-x;}
#files .image .onion-skin .controls .dragger,.file-box .image .onion-skin .controls .dragger{display:block;position:absolute;left:0;top:0;height:14px;width:14px;background:url(/images/modules/commit/onion_skin_sprites.gif) 0 -34px repeat-x;cursor:pointer;}
#files .image .onion-skin .controls .dragger:hover,.file-box .image .onion-skin .controls .dragger:hover{background-position:0 -48px;}
#files .image .difference .added-frame,.file-box .image .difference .added-frame{display:none;}
#files .image .difference .deleted-frame,.file-box .image .difference .deleted-frame{border-color:#999;}
.file-editor-textarea{padding:4px;width:908px;border:1px solid #eee;font:12px Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;}
textarea.commit-message{margin:10px 0;padding:4px;width:910px;height:50px;font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:14px;border:1px solid #ddd;}
.commit-message-label{display:block;margin-bottom:-5px;color:#666;}
.check-for-fork{display:none;}
.blame{background-color:#f8f8f8!important;}
.blame table tr td{padding:.2em .5em;}
.blame .commit-date{color:#888;}
.blame table tr.section-first td{border-top:1px solid #ccc;}
.blame .line-number{background-color:#ececec;color:#aaa;padding:0 .5em;text-align:right;border-left:1px solid #ddd;border-right:1px solid #ddd;}
.blame .line-data{background-color:#f8f8ff;white-space:pre;}
.blame .commitinfo code{font-size:12px;}
.blame .commitinfo .date{color:#666;}
#dashboard{margin-top:-10px;overflow:hidden;}
#dashboard h1{font-size:160%;margin-bottom:.5em;}
#dashboard h1 a{font-size:70%;font-weight:normal;}
.news{float:left;margin-top:15px;width:560px;}
.page-profile .news{float:none;width:auto;}
.news blockquote{color:#666;}
.news pre,.news code{font-family:Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;font-size:90%;}
.news h1{margin-bottom:0;}
.filter,.feed_filter{border-bottom:1px solid #AAA;padding-bottom:.25em;margin-bottom:1em;}
.filter li,.feed_filter li{clear:none;display:inline;}
.news .alert{padding:0 0 1em 2em;overflow:hidden;}
.news .alert p{margin:0;}
.news .alert .body{border-bottom:1px solid #ccc;overflow:hidden;padding:0 0 1em 0;}
.news .alert .title{padding:0 0 .25em 0;font-weight:bold;}
.news .alert .title span{background-color:#fff6a9;}
.news .alert .title .subtle{color:#bbb;}
.news .alert .gravatar{border:1px solid #d0d0d0;padding:2px;background-color:white;float:left;line-height:0;margin-right:.7em;}
.news .commit{background:url(/images/modules/dashboard/news/commit.png) no-repeat;}
.news .commit_comment{background:url(/images/modules/dashboard/news/comment.png) no-repeat;}
.news .create{background:url(/images/modules/dashboard/news/create.png) no-repeat;}
.news .public{background:url(/images/modules/dashboard/news/public.png) no-repeat;}
.news .git_hub{background:url(/images/modules/dashboard/news/site.png) no-repeat;}
.news .git_hub .done{text-decoration:line-through;color:#666;}
.news .delete{background:url(/images/modules/dashboard/news/delete.png) no-repeat;}
.news .pull_request{background:url(/images/modules/dashboard/news/pull_request.png) no-repeat;}
.news .fork{background:url(/images/modules/dashboard/news/fork.png) no-repeat;}
.news .fork_apply{background:url(/images/modules/dashboard/news/merge.png) no-repeat;}
.news .follow{background:url(/images/modules/dashboard/news/follow.png) no-repeat;}
.news .issues_opened{background:url(/images/modules/dashboard/news/issues_opened.png) no-repeat;}
.news .issues_closed{background:url(/images/modules/dashboard/news/issues_closed.png) no-repeat;}
.news .issues_reopened{background:url(/images/modules/dashboard/news/issues_reopened.png) no-repeat;}
.news .issues_comment{background:url(/images/modules/dashboard/news/issues_comment.png) no-repeat;}
.news .gist{background:url(/images/modules/dashboard/news/gist.png) no-repeat;}
.news .guide{background:url(/images/modules/dashboard/news/wiki.png) no-repeat;}
.news .gollum,.news .wiki{background:url(/images/modules/dashboard/news/wiki.png) no-repeat;}
.news .team_add{background:url(/images/modules/dashboard/news/member_add.png) no-repeat;}
.news .member_add{background:url(/images/modules/dashboard/news/member_add.png) no-repeat;}
.news .member_remove{background:url(/images/modules/dashboard/news/member_remove.png) no-repeat;}
.news .watch_started{background:url(/images/modules/dashboard/news/watch_started.png) no-repeat;}
.news .watch_stopped{background:url(/images/modules/dashboard/news/watch_stopped.png) no-repeat;}
.news .delete{background:url(/images/modules/dashboard/news/delete.png) no-repeat;}
.news .push{background:url(/images/modules/dashboard/news/push.png) no-repeat;height:auto;}
.news .download{background:url(/images/modules/dashboard/news/download.png) no-repeat;}
.news .commits li{margin-left:3.5em;margin-top:.25em;list-style-type:none;}
.news .commits li .committer{padding-left:.5em;display:none;}
.news .commits li img{border:1px solid #d0d0d0;padding:1px;vertical-align:middle;background-color:white;margin:0 3px;}
.news .commits li img.emoji{border:0;padding:0;margin:0;}
.news div.message,.news li blockquote{display:inline;color:#444;}
.news .commits li.more{padding-top:2px;padding-left:2px;}
.profilecols .news .push li{margin-left:0;}
#dashboard .followers{float:right;width:35em;margin-bottom:2em;}
#dashboard .followers h1{margin-bottom:.3em;border-bottom:1px solid #ddd;}
#dashboard .followers ul{list-style-type:none;}
#dashboard .followers ul li{display:inline;}
#dashboard .followers ul li img{border:1px solid #d0d0d0;padding:1px;}
#dashboard .news.public_news{float:right;width:35em;}
#dashboard .news.public_news h1{margin-bottom:.3em;border-bottom:1px solid #ddd;}
#dashboard .repos{float:right;clear:right;}
#dashboard .repos h1{margin-bottom:0;}
#dashboard .repos img{vertical-align:middle;}
#dashboard .dossier{float:left;width:32.18em;margin-bottom:2em;}
#dashboard .dossier .profile .identity{overflow:hidden;}
#dashboard .dossier .profile .identity img{border:1px solid #d0d0d0;padding:2px;background-color:white;float:left;margin-right:.7em;}
#dashboard .dossier .profile .identity h1{line-height:56px;}
#dashboard .dossier .profile .buttons{margin-bottom:1.3em;}
#dashboard .dossier .profile .vcard{border:1px solid #888;background-color:#F8FFD5;}
#dashboard .dossier .profile .vcard .info{font-size:90%;}
#dashboard .dossier .profile .vcard .field{overflow:hidden;}
#dashboard .dossier .profile .vcard .field label{float:left;margin-right:1em;display:block;text-align:right;width:8em;color:#777;padding:.1em 0;}
#dashboard .dossier .profile .vcard .field div{float:left;}
#dashboard .dossier .profile .vcard .field a.action{color:#a00;}
#dashboard .projects{margin-top:2em;list-style-type:none;}
#dashboard .projects.floated li{float:left;margin-right:2em;}
#dashboard .projects .project{border:1px solid #d8d8d8;background-color:#f0f0f0;margin-bottom:1em;padding:0 .4em;}
#dashboard .projects .project .title{font-size:140%;}
#dashboard .projects .project .meta{margin:.2em 0 0 0;font-style:italic;color:#888;}
#dashboard .projects .project .graph{margin:.5em 0;}
#dashboard .projects .project .graph .bars{width:31.18em;height:20px;}
#dashboard .projects .project .graph img.legend{width:31.18em;}
#dashboard .projects .project .flexipill{float:right;padding-top:.3em;margin-right:.5em;}
#dashboard .projects .project .flexipill a{color:black;}
#dashboard .projects .project .flexipill .middle{background:url(/images/modules/repos/pills/middle.png) 0 0 repeat-x;padding:0 0 0 .3em;}
#dashboard .projects .project .flexipill .middle span{position:relative;top:.1em;font-size:95%;}
.editbox{border-left:1px solid #ccc;border-top:1px solid #ccc;border-right:1px solid #ccc;background-color:#f8f8ff;margin-top:1.5em;}
.editbox .hint{font-style:italic;color:#888;margin:.3em 0;padding-top:.5em;border-top:1px solid #ccc;}
.editbox textarea{border:1px solid #888;padding:4px;}
.editbox input.text{border:1px solid #888;padding:4px;}
.editbox .fail{color:#a00;}
.editbox .succeed{color:#0a0;}
.editbox h1{padding:.5em;border-bottom:1px solid #ccc;background-color:#eee;font-size:100%;overflow:hidden;}
.editbox h1 strong{float:left;}
.editbox .body{padding:0 .5em;border-bottom:1px solid #ccc;}
.editbox .body p{margin:.5em 0;}
.editbox .body ul{margin:.5em;list-style-type:none;}
#keys h1 a{float:right;font-weight:normal;}
#keys .danger{font-weight:bold;color:#a00;}
#keys ul{list-style:none;}
#keys ul li{font-weight:bold;margin:.5em 0;}
#keys ul li a{font-weight:normal;}
#keys .key_editing textarea{width:36em;height:14em;display:block;margin-bottom:.7em;}
#keys .key_editing .object_error{color:#a00;border:1px solid #a00;background-color:#f2e1e1;padding:.5em;margin-top:.5em;}
#keys label{display:block;margin:.5em 0;color:#888;font-size:90%;}
#keys textarea{width:36em;height:12em;display:block;margin-bottom:.7em;}
#facebox .key_editing textarea{width:32.5em;height:10em;}
#facebox .key_editing .object_error{color:#a00;margin:0 1em 1em 1em;border:1px solid #a00;background-color:#f2e1e1;padding:.5em;}
#receipts table{width:100%;border-left:1px solid #ccc;border-top:1px solid #ccc;border-right:1px solid #ccc;}
#receipts table th{padding:.4em;border-bottom:1px solid #ccc;color:#333;background-color:#eee;}
#receipts table td{padding:.4em;border-bottom:1px solid #ccc;}
#receipts table tr.success td{background-color:#EFFFED;}
#receipts table tr.failure td{background-color:#FFEDED;}
#receipts table td.empty{color:#a00;font-weight:bold;text-align:center;}
#receipts table td.date{color:#888;}
#receipts table tr.success td.amount{color:#0a0;font-weight:bold;}
#receipts table tr.failure td.amount{color:#a00;font-weight:bold;}
#watchers{margin:15px 0;border-top:1px solid #ddd;}
#watchers li{border-bottom:1px solid #ddd;}
ul.members{list-style:none;}
.members li{position:relative;font-size:14px;margin:0;padding:5px 0;height:24px;line-height:24px;font-weight:bold;}
.members li em{font-style:normal;color:#999;}
.members li a.follow{position:absolute;top:5px;right:0;}
.members li .gravatar{border:1px solid #ddd;padding:1px;background-color:white;float:left;margin-right:10px;}
#directory.compact{width:50em;}
#directory .news{width:100%;}
#directory h1{border-bottom:1px solid #aaa;margin-bottom:.5em;}
#directory .news h1{border-bottom:none;margin-bottom:0;}
#directory .repo{width:100%;}
#directory .repo .gravatar{width:50px;}
#directory .repo .gravatar img{border:1px solid #d0d0d0;padding:1px;background-color:white;}
#directory .repo .title{font-size:140%;}
#directory .repo .owner,#directory .repo .date{text-align:center;}
#directory .repo .graph{width:426px;vertical-align:top;padding-top:.2em;text-align:right;}
#directory .repo .sep{font-size:50%;}
#directory .repo .border{border-bottom:1px solid #ddd;}
#guides h1{margin-bottom:.5em;}
#guides .index ul{list-style-type:none;font-size:120%;}
#guides .index ul li{padding-left:1.5em;background:white url(/images/modules/guides/book.png) no-repeat;}
#guides .index .new{margin-top:1em;border-top:1px solid #ccc;padding-top:.5em;}
#guides .index .new ul li{background:white url(/images/modules/guides/book_add.png) no-repeat;}
#guides .index .new ul li a{color:#c00;}
#guides .write .delete_page{float:right;}
#guides .guide{overflow:hidden;}
#guides .guide .main{float:left;width:50em;}
#guides .guide .sidebar{float:right;width:15em;border-left:4px solid #e6e6e6;margin:2.1em 0 0 0;padding-left:1em;}
#guides .guide .sidebar h3{margin:0 0 .5em 0;}
#guides .guide .sidebar ul{list-style-type:none;margin:0;color:#888;}
#guides .guide .sidebar ul li{padding-left:12px;background:white url(/images/modules/guides/sidebar/bullet_blue.png) -4px 0 no-repeat;margin:.2em 0;}
#guides .admin{clear:both;margin-top:3em;border-top:4px solid #e6e6e6;padding-top:.3em;overflow:hidden;}
#guides .write label{font-size:110%;color:#666;display:block;margin:1em 0;}
#guides .write input.text,#guides .write textarea{padding:5px;border:1px solid #888;}
#guides .write input.text{width:40em;}
#guides .write textarea{width:100%;height:25em;}
#guides .write label span.title{color:black;font-weight:bold;}
#guides .write .actions input{margin-right:1em;}
#guides .write #preview_bucket{border:1px solid #888;background-color:white;padding:5px;}
#network h2{margin-bottom:.25em;}
#network p{font-size:120%;margin:1em 0;}
#network .repo{font-size:140%;}
#network .repo img{vertical-align:middle;}
#network .repo img.gravatar{padding-right:4px;padding:1px;border:1px solid #ccc;background-color:white;}
#network .repo span{background-color:#FFF6A9;}
#network .repo a.commit{color:#888;font-size:80%;line-height:1em;}
#network .help_actions{margin-left:5px;}
#network .help_actions a{font-size:12px;}
#network #help pre{font-size:80%;line-height:1.2em;margin-bottom:1.5em;border:1px solid black;color:#eee;background-color:#222;padding:1em;}
#network .notice{border:1px solid #EFCF00;background-color:#FFFAD6;padding:.5em;color:#837200;text-align:center;}
#network .explain{color:#666;font-size:13px;font-style:italic;margin:-5px 0 20px 2px;}
#network .explain b{color:#333;font-weight:normal;}
#network .graph-date{text-align:right;margin:-30px 4px 5px 0;color:#555;font-size:12px;}
#network .graph-date abbr{font-style:normal;color:#444;}
.facebox p{margin:.5em 0;}
.facebox b{background-color:#FFF6A9;}
.facebox ul{margin-left:1em;}
.facebox ol{margin-left:1.5em;}
#pull_request ul{list-style-type:none;}
#pull_request label.repo span.name{font-size:160%;}
#pull_request label.repo span span.sha{color:#aaa;}
#pull_request .label label{display:inline;margin:0;font-size:100%;font-weight:bold;}
#pull_request .label div{margin:.2em;0;}
#pull_request .recipients{max-height:200px;overflow:auto;}
#training_sections{margin-bottom:1.5em;font-size:110%;}
#training_sections h3{margin-top:2.5em;}
#training_sections img.training_pic{float:right;padding:5px;margin:5px 20px;}
#training_contact{border-top:1px solid #aaa;padding-top:.9em;}
#training_testimonials{border-top:2px solid #aaa;padding:1.5em;background:#eee;}
#training_testimonials h1{text-align:center;font-size:150%;}
#training_contact h2{text-align:center;}
.testimony{margin:1em auto;font-size:120%;font-style:italic;color:#666;clear:both;max-width:600px;padding:10px;}
.testimony .author{font-style:normal;text-align:right;color:#000;font-size:100%;}
.blog-comments .comment-form{margin-top:0;}
#posts{margin-top:1.5em;overflow:hidden;padding-top:.5em;}
#posts .list{float:left;width:41em;}
#posts li.post{list-style-type:none;margin-bottom:2em;}
#posts h2{margin:0;font-size:190%;}
#posts h3{margin:1em 0 .5em 0;}
#posts .meta .who_when{font-size:130%;}
#posts .meta .who_when img,img.who_when{vertical-align:middle;padding:1px;border:1px solid #ccc;position:relative;top:-1px;}
#posts .meta .who_when .author a{color:#94bfea;font-weight:bold;}
#posts .meta .who_when .published a,#posts .meta .who_when .published{color:#ccc;}
#posts .meta .who_when .status{color:#a00;}
#posts .meta .respond{margin:.3em 0;padding-left:25px;background:transparent url(/images/modules/posts/bubble.png) 0 50% no-repeat;font-size:110%;}
#posts .meta .respond a{color:#cbb698;}
#posts .entry-content{font-size:110%;margin-top:1em;}
#posts .entry-content blockquote{padding-left:1em;color:#666;}
#posts .entry-content p{margin:1em 0;}
#posts .entry-content pre{background-color:#f8f8f8;border:1px solid #ddd;font-size:90%;padding:.5em;}
#posts .entry-content pre code{background-color:#f8f8f8;font-size:95%;}
#posts .entry-content code{font-size:90%;background-color:#ddd;padding:0 .2em;}
#posts .entry-content img{margin:1em 0;padding:.3em;border:1px solid #ddd;max-width:540px;}
#posts .entry-content img.emoji{margin:0;padding:0;border:0;}
#posts .entry-content p img{margin:0;}
#posts .entry-content ul{margin-left:1.25em;}
#posts .entry-content ol{margin-left:2em;}
#posts .entry-content ul li{margin:.5em 0;}
#posts .comments .comment .body img{max-width:39em;}
#posts .sidebar{float:right;width:26em;}
#posts .sidebar .rss{text-align:center;}
#posts .sidebar .others{border-top:2px solid #eee;margin-top:.75em;padding-top:.75em;}
#posts .sidebar .others h3{margin-top:.25em;}
#posts .sidebar .others ul{list-style-type:none;}
#posts .sidebar .others li{padding:.5em 0;}
#posts .sidebar .others li a{font-size:140%;line-height:1em;}
#posts .sidebar .others .meta{color:#888;}
.iphone #posts .list{width:100%;}
#new_comment textarea{height:10em;}
#posts pre{margin:1em 0;font-size:12px;background-color:#f8f8ff;border:1px solid #dedede;padding:.5em;line-height:1.5em;color:#444;overflow:auto;}
#posts pre code{padding:0;font-size:12px;background-color:#f8f8ff;border:none;}
#posts code{font-size:12px;background-color:#f8f8ff;color:#444;padding:0 .2em;border:1px solid #dedede;}
.commentstyle{border:2px solid #e4e4e4;border-bottom:none;background-color:#f5f5f5;overflow:hidden;}
.commentstyle .previewed .comment{background-color:#FFFED6;}
.commentstyle .comment{border-bottom:2px solid #e4e4e4;padding:.5em;}
.commentstyle .comment .meta{margin-bottom:.4em;}
.commentstyle .comment .meta .gravatar{padding:1px;border:1px solid #ccc!important;vertical-align:middle;}
.commentstyle .comment .meta span{vertical-align:middle;color:#aaa;}
.commentstyle .comment .meta .date{font-style:italic;color:#555;}
.commentstyle .comment .body{padding:0 0 0 .2em;}
.commentstyle form{padding:.5em;}
.commentstyle form textarea{height:5em;width:100%;margin-bottom:.5em;}
.commentstyle form .status{color:#a00;font-weight:bold;}
.commentstyle form .actions{overflow:hidden;}
.commentstyle form .actions .submits{float:left;}
.commentstyle form .actions .formatting{float:right;font-size:90%;color:#666;}
#tour{margin-top:2em;}
#tour .site{width:67.62em;}
#tour .movie{padding:1px;background-color:#ddd;border:1px solid #bbb;}
#tour .movie img{width:898px;height:395px;}
#tour .sections{overflow:hidden;margin-top:2em;}
#tour .sections .section{width:22.5em;float:left;}
#tour .sections .section h2{font-size:200%;}
#tour .sections .section ul{list-style-type:none;font-size:140%;}
#tour .sections .section ul li{line-height:1.5em;color:#aaa;padding-left:1.1em;background:transparent url(/images/modules/tour/play_bullet.png) 0 45% no-repeat;}
#tour .sections .section ul li a{color:black;text-decoration:underline;}
#tour .signup{text-align:center;margin-top:4em;}
.pagination{padding:.3em;margin:.3em;}
.pagination a{padding:.1em .3em;margin:.2em;border:1px solid #aad;text-decoration:none;color:#369;}
.pagination a:hover,.pagination a:active{border:1px solid #369;color:#000;}
.pagination span.current{padding:.1em .3em;margin:.2em;border:1px solid #369;font-weight:bold;background-color:#369;color:#FFF;}
.pagination span.disabled{padding:.1em .3em;margin:.2em;border:1px solid #eee;color:#ddd;}
.ajax_paginate a{padding:.5em;width:100%;text-align:center;display:block;}
#commit_comments{width:50em;}
#commit_comments h1{margin-bottom:0;}
#commit_comments .inner{margin:0;padding:0;}
#commit_comments .body{background-color:transparent;width:100%;}
#commit_comments .no_one{margin-left:.5em;margin-bottom:0;font-weight:bold;}
#commit_comments textarea{width:97.5%;}
#commit_comments .actions{border-top:none;padding:0;}
#archives h2{color:#666;margin-bottom:15px;padding-bottom:5px;}
#archives h2 span.owner{color:#000;}
#archives h4{border-bottom:1px solid #ddd;color:#666;font-size:10px;margin-bottom:7px;padding-bottom:0;text-shadow:0 -1px 0 #fff;text-transform:uppercase;}
#archives .source-downloads{margin-bottom:20px;}
#archives .source-downloads .minibutton{margin-right:5px;}
#archives .source-downloads .current-branch{font-size:10px;font-weight:bold;display:inline-block;margin:0 5px 0 0;}
#archives .source-downloads .current-branch code{font-size:10px;font-weight:normal;}
#archives .other-downloads h4{margin-bottom:0;}
#archives .other-downloads ul{list-style-type:none;margin:0;}
#archives .other-downloads ul li{border-bottom:1px solid #ddd;margin:0;padding:6px 10px 5px;}
#archives .other-downloads ul li.featured{font-weight:bold;}
#archives .other-downloads ul li.tagged-download{background-image:url(/images/icons/tag.png);background-position:10px 5px;background-repeat:no-repeat;padding-left:33px;}
#archives .wait{padding:2em 0 3em 0;}
#archives .wait h2,#archives .wait p{text-align:center;}
#services .test_hook{margin-top:.5em;}
#privacy_terms h1{margin-bottom:.3em;}
#privacy_terms h2{margin-top:1em;}
#privacy_terms ul,#privacy_terms ol{margin-left:1.4em;}
#privacy_terms p{margin-bottom:1em;}
#languages .popular{background-color:#fdfdfd;overflow:hidden;margin:15px 0;}
#languages .popular h3{font-size:105%;color:#aaa;margin-bottom:.5em;}
#languages .popular .site .left img{border:1px solid #d0d0d0;padding:1px;background-color:white;margin-right:.1em;position:absolute;top:.25em;left:0;}
#languages .popular a{color:black;}
#languages .popular ul{list-style-type:none;}
#languages .popular ul li{line-height:1.6em!important;font-size:125%;color:#888;padding-left:1.6em;position:relative;}
#languages .popular ul li a.repo{font-weight:bold;}
#languages .popular .left{margin-left:14em;float:left;width:27em;}
#languages .popular.compact .left{margin-left:0;float:left;width:25em;padding-bottom:2em;}
#languages .popular.compact .left.row{clear:left;}
#languages .all_languages{padding-right:3em;text-align:right;}
#languages a.bar{display:block;color:#fff;text-decoration:none;padding:3px;background-color:#4183C4;min-width:20px;border-top-right-radius:4px;border-bottom-right-radius:4px;-moz-border-radius-topright:4px;-moz-border-radius-bottomright:4px;-webkit-border-top-right-radius:8px;-webkit-border-bottom-right-radius:8px;}
#language_table{border:1px solid #eee;}
#language_table th{background:#f0f0f0;padding:.5em;}
#language_table td{padding:.5em;}
#language_table tr.dark{background:#fafafa;}
.ac_results{-moz-border-radius:8px;-webkit-border-radius:8px;border-radius:8px;padding:3px;}
.ac_results ul li:first-child{-moz-border-radius-topright:8px;-moz-border-radius-topleft:8px;-webkit-border-top-right-radius:8px;-webkit-border-top-left-radius:8px;border-top-right-radius:8px;border-top-left-radius:8px;}
.ac_results ul li:last-child{-moz-border-radius-bottomright:8px;-moz-border-radius-bottomleft:8px;-webkit-border-bottom-right-radius:8px;-webkit-border-bottom-left-radius:8px;border-bottom-right-radius:8px;border-bottom-left-radius:8px;}
.ac_results img{padding:1px;background-color:white;border:1px solid #ccc;vertical-align:middle;}
.error-notice{margin:15px 0;text-align:center;font-size:14px;font-weight:bold;color:#900;}
.error-notice span{padding-left:30px;background:url(/images/icons/error_notice.png) 0 50% no-repeat;}
.inline-edit textarea{width:100%;height:50px;}
.inline-edit .textfield{width:400px;font-size:12px;padding:5px;color:#666;}
.inline-edit .form-actions{margin-top:5px;text-align:left;}
.inline-edit .form-actions .cancel{float:none;color:#900;}
.entice{opacity:.5;}
.clippy-tooltip{display:inline-block;}
#files{position:relative;}
#files .add-bubble{position:absolute;left:0;width:30px;height:14px;margin-left:-30px;margin-top:3px;background:url(/images/modules/comments/add_bubble.png) 0 0 no-repeat #fff;cursor:pointer;opacity:0;filter:alpha(opacity=0);-webkit-transition:opacity .1s linear;}
#files tr:hover .add-bubble{opacity:1.0;filter:alpha(opacity=100);}
#files.commentable tr:hover td,#files.commentable tr:hover td .gd,#files.commentable tr:hover td .gi,#files.commentable tr:hover td .gc{background-color:#ffc;}
#files.commentable tr:hover td.line_numbers a,#files.commentable tr:hover td.line_numbers span{color:#555!important;}
table.padded{font-size:1.3em;}
table.padded tr th{background:#eee;text-align:right;padding:8px 15px;}
table.padded tr td{text-align:left;padding:8px;}
.page-notice{margin:15px auto;width:400px;padding:20px;color:#333;font-size:14px;background:#fffeeb;border:1px solid #ddd;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px;}
.page-notice h2{margin:0;font-size:16px;color:#000;}
.page-notice p:last-child{margin-bottom:0;}
.ac-accept{background:#DDFFDA url(/images/icons/accept.png) 100% 50% no-repeat;}
.trans table{width:100%;}
.trans table tr th{color:#333;font-size:120%;border-bottom:1px solid #333;}
.trans table tr td{border-bottom:1px solid #eee;padding:4px;}
.trans table tr td .info{font-size:80%;color:#777;}
.trans table tr td .date{color:#777;}
.trans table tr td .langname a{font-size:120%;color:#282;font-weight:bold;}
.trans table tr td .percent{border:1px solid #89a;width:95%;}
.trans table tr td a.bar{display:block;color:#fff;text-decoration:none;padding:3px;background-color:#4183c4;min-width:10px;}
.trans table tr td a.sadbar{background-color:#bbb;}
.trans .infobox{border:1px solid #aaa;background:#eee;padding:5px;margin:10px;color:#444;}
.trans table.short{width:600px;}
.trans h2{background:#eee;padding:3px;}
.trans .hint{color:#777;}
.trans_next table{width:600px;margin-bottom:10px;}
.trans_next table tr th{padding:8px;border-bottom:1px solid #ccc;background:#eee;}
.trans_next table tr td{padding:8px;border-bottom:1px solid #eee;width:75%;}
.translate_box{width:600px;}
.translate_box #loading{padding:30px;}
.trans table tr td code{font-size:12px;}
input.tree-finder-input{border:0;outline:none;font-size:100%;}
.tree-finder .results-list tr.current td{background:#eee;}
.tree-finder .no-results th{text-align:center;}
.tree-finder tr td.icon{cursor:pointer;}
#slider{position:relative;overflow:hidden;}
#slider .frames{width:10000px;}
#slider .frames .frame{float:left;width:920px;margin-right:100px;}
#slider .frames .frame-loading{height:100%;}
#files .file{margin-top:0;}
#slider .frames .big-actions{position:absolute;top:15px;right:0;margin:0;}
#wiki-wrapper{margin:0 auto 50px 0;overflow:visible;font-size:10px;line-height:normal;}
#wiki-wrapper #head{border-bottom:1px solid #ccc;margin:14px 0 5px;padding:.5em 0;overflow:hidden;}
#wiki-wrapper #head h1{font-size:33px;float:left;line-height:normal;margin:0;padding:.08em 0 0 0;width:65%;}
#wiki-wrapper #head ul.actions{float:right;margin-top:.6em;}
#wiki-wrapper #wiki-content{height:1%;overflow:hidden;}
#wiki-wrapper #wiki-content .wrap{height:1%;width:100%;}
#wiki-wrapper #wiki-content .wrap:after{content:".";display:block;height:0;clear:both;visibility:hidden;}
#wiki-wrapper #wiki-body{float:left;width:100%;}
#wiki-wrapper .has-rightbar #wiki-body{float:left;margin-right:3%;width:65%;}
#wiki-rightbar{background-color:#f7f7f7;border:1px solid #ddd;float:right;margin-top:1.5em;padding:1em;width:25%;border-radius:.5em;-moz-border-radius:.5em;-webkit-border-radius:.5em;}
#wiki-wrapper #wiki-rightbar>*:first-child{margin-top:0;}
#wiki-wrapper #wiki-rightbar #nav{font-size:1.2em;line-height:1.5em;}
#wiki-wrapper #wiki-rightbar #nav p.parent{border-bottom:1px solid #bbb;font-weight:bold;margin:0 0 .5em 0;padding:0 0 .5em 0;text-shadow:0 1px 0 #fff;}
#wiki-wrapper #wiki-rightbar #nav p.parent:before{color:#666;content:"← ";}
#wiki-wrapper #wiki-rightbar #nav h3{font-size:1.2em;color:#333;margin:1.2em 0 0;padding:0;text-shadow:0 1px 0 #fff;}
#wiki-wrapper #wiki-rightbar ul,#wiki-wrapper #wiki-rightbar ol{margin:.5em 0 0 1.5em;padding:0;}
#wiki-wrapper #wiki-rightbar ul{list-style-type:square;}
#wiki-wrapper #wiki-rightbar ul li,#wiki-wrapper #wiki-rightbar ol li{color:#333;font-size:1.2em;margin:0;padding:0;line-height:1.6em;}
#wiki-wrapper #wiki-rightbar ul li a,#wiki-wrapper #wiki-rightbar ol li a{font-weight:bold;text-shadow:0 1px 0 #fff;}
#wiki-wrapper #wiki-rightbar p{font-size:1.2em;line-height:1.6em;}
#wiki-wrapper #wiki-footer{clear:both;margin:2em 0 5em;}
#wiki-wrapper .has-rightbar #wiki-footer{width:65%;}
#wiki-wrapper #wiki-footer #gollum-footer-content{background-color:#f7f7f7;border:1px solid #ddd;font-size:1.2em;line-height:1.5em;margin-top:1.5em;padding:1em;border-radius:.5em;-moz-border-radius:.5em;-webkit-border-radius:.5em;}
#wiki-wrapper #wiki-footer #gollum-footer-content>*:first-child{margin-top:0;}
#wiki-wrapper #wiki-footer #gollum-footer-content h3{font-size:1.2em;color:#333;margin:0;padding:0 0 .2em;text-shadow:0 1px 0 #fff;}
#wiki-wrapper #wiki-footer #gollum-footer-content p{margin:.5em 0 0;padding:0;}
#wiki-wrapper #wiki-footer #gollum-footer-content ul,#wiki-wrapper #wiki-footer #gollum-footer-content ol{margin:.5em 0 0 1.5em;}
#wiki-wrapper #wiki-footer #gollum-footer-content ul.links{margin:.5em 0 0;overflow:hidden;padding:0;}
#wiki-wrapper #wiki-footer #gollum-footer-content ul.links li{color:#999;float:left;list-style-position:inside;list-style-type:square;padding:0;margin-left:.75em;}
#wiki-wrapper #wiki-footer #gollum-footer-content ul.links li a{font-weight:bold;text-shadow:0 1px 0 #fff;}
#wiki-wrapper #wiki-footer #gollum-footer-content ul.links li:first-child{list-style-type:none;margin:0;}
#wiki-wrapper .ff #wiki-footer #gollum-footer-content ul.links li:first-child{margin:0 -0.75em 0 0;}
#wiki-wrapper .page #gollum-footer{border-top:1px solid #ccc;margin:1em 0 7em;}
#wiki-wrapper #gollum-footer p#last-edit{font-size:1.2em;line-height:1.6em;color:#999;margin:.9em 0 0;}
#wiki-wrapper #gollum-footer p#last-edit span.username{font-weight:bold;}
#wiki-wrapper #gollum-footer p#delete-link{font-size:1.2em;line-height:1.6em;margin:0 0 .9em 0;}
#wiki-wrapper.history h1{color:#999;font-weight:normal;}
#wiki-wrapper.history h1 strong{color:#000;font-weight:bold;line-height:normal;}
#wiki-wrapper #wiki-history{margin-top:3em;}
#wiki-wrapper #wiki-history fieldset{border:0;margin:2em 0;padding:0;}
#wiki-wrapper #wiki-history table,#wiki-history tbody{border-collapse:collapse;padding:0;margin:0;width:100%;}
#wiki-wrapper #wiki-history table tr{padding:0;margin:0;}
#wiki-wrapper #wiki-history table tr{background-color:#ebf2f6;}
#wiki-wrapper #wiki-history table tr td{border:1px solid #c0dce9;font-size:1.2em;line-height:1.6em;margin:0;padding:.3em .7em;}
#wiki-wrapper #wiki-history table tr td.checkbox{min-width:2em;width:2em;padding:.3em 0 .2em .8em;}
#wiki-wrapper #wiki-history table tr td.checkbox input{cursor:pointer;display:block;margin:0;padding:0;}
#wiki-wrapper #wiki-history table tr:nth-child(2n),#wiki-wrapper #wiki-history table tr.alt-row{background-color:#f3f7fa;}
#wiki-wrapper #wiki-history table tr.selected{background-color:#ffffea!important;z-index:100;}
#wiki-wrapper #wiki-history table tr td.commit-name{border-left:0;}
#wiki-wrapper #wiki-history table tr td.commit-name span.time-elapsed{color:#999;}
#wiki-wrapper #wiki-history table tr td.author{width:20%;}
#wiki-wrapper #wiki-history table tr td.author a{color:#000;font-weight:bold;}
#wiki-wrapper #wiki-history table tr td.author a span.username{display:block;padding-top:3px;}
#wiki-wrapper #wiki-history table tr td img{background-color:#fff;border:1px solid #999;display:block;float:left;height:18px;overflow:hidden;margin:0 .5em 0 0;width:18px;padding:2px;}
#wiki-wrapper #wiki-history table tr td.commit-name a{font-size:.9em;font-family:Consolas,Monaco,"DejaVu Sans Mono","Bitstream Vera Sans Mono","Courier New",monospace;padding:0 .2em;}
#wiki-wrapper.history #wiki-history ul.actions li,#wiki-wrapper.history #gollum-footer ul.actions li{margin:0 .6em 0 0;}
#wiki-wrapper.edit h1{color:#999;font-weight:normal;}
#wiki-wrapper.edit h1 strong{color:#000;font-weight:bold;line-height:normal;}
#wiki-wrapper.results h1{color:#999;font-weight:normal;}
#wiki-wrapper.results h1 strong{color:#000;font-weight:bold;line-height:normal;}
#wiki-wrapper.results #results{border-bottom:1px solid #ccc;margin-bottom:2em;padding-bottom:2em;}
#wiki-wrapper .results #results ul{margin:2em 0 0 0;padding:0;}
#wiki-wrapper .results #results ul li{font-size:1.2em;line-height:1.6em;list-style-position:outside;padding:.2em 0;}
#wiki-wrapper .results #results ul li span.count{color:#999;}
#wiki-wrapper .results p#no-results{font-size:1.2em;line-height:1.6em;margin-top:2em;}
#wiki-wrapper .results #gollum-footer ul.actions li{margin:0 1em 0 0;}
#wiki-wrapper.compare h1{color:#000;font-weight:bold;}
#wiki-wrapper.compare #compare-content{margin-top:3em;}
#wiki-wrapper.compare #compare-content ul.actions li,#wiki-wrapper.compare #gollum-footer ul.actions li{margin-left:0;margin-right:.6em;}
#wiki-wrapper.compare #compare-content ul.actions{margin-bottom:1.4em;}
#wiki-wrapper ul.actions{display:block;list-style-type:none;overflow:hidden;padding:0;}
#wiki-wrapper ul.actions li{float:left;font-size:1.2em;margin-left:.6em;}
#wiki-wrapper .gollum-minibutton a{background-color:#f7f7f7;border:1px solid #d4d4d4;color:#333;display:block;font-weight:bold;margin:0;padding:.4em 1em;height:1.4em;text-shadow:0 1px 0 #fff;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#f4f4f4),to(#ececec));background:-moz-linear-gradient(top,#f4f4f4,#ececec);border-radius:3px;-moz-border-radius:3px;-webkit-border-radius:3px;}
#wiki-wrapper #search-submit{background-color:#f7f7f7;border:1px solid #d4d4d4;color:#333;display:block;font-weight:bold;margin:0;padding:.4em 1em;text-shadow:0 1px 0 #fff;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#f4f4f4),to(#ececec));background:-moz-linear-gradient(top,#f4f4f4,#ececec);border-radius:3px;-moz-border-radius:3px;-webkit-border-radius:3px;}
#wiki-wrapper .gollum-minibutton a:hover,#wiki-wrapper #search-submit:hover{background:#3072b3;border-color:#518cc6 #518cc6 #2a65a0;color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,0.3);text-decoration:none;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#599bdc',endColorstr='#3072b3');background:-webkit-gradient(linear,left top,left bottom,from(#599bdc),to(#3072b3));background:-moz-linear-gradient(top,#599bdc,#3072b3);}
#wiki-wrapper .gollum-minibutton a:visited{text-decoration:none;}
#wiki-wrapper.error{height:1px;position:absolute;overflow:visible;top:50%;width:100%;}
#wiki-wrapper #error{background-color:#f9f9f9;border:1px solid #e4e4e4;left:50%;overflow:hidden;padding:2%;margin:-10% 0 0 -35%;position:absolute;width:70%;border-radius:.5em;-moz-border-radius:.5em;-webkit-border-radius:.5em;}
#wiki-wrapper #error h1{font-size:3em;line-height:normal;margin:0;padding:0;}
#wiki-wrapper #error p{font-size:1.2em;line-height:1.6em;margin:1em 0 .5em;padding:0;}
#wiki-wrapper .jaws{display:block;height:1px;left:-5000px;overflow:hidden;position:absolute;top:-5000px;width:1px;}
#wiki-wrapper #gollum-editor{border:1px solid #e4e4e4;background:#f9f9f9;margin:1em 0 5em;overflow:hidden;padding:1em;border-radius:1em;-moz-border-radius:1em;-webkit-border-radius:1em;}
#wiki-wrapper .ie #gollum-editor{padding-bottom:1em;}
#wiki-wrapper #gollum-editor form fieldset{border:0;margin:0;padding:0;width:100%;}
#wiki-wrapper #gollum-editor .singleline{display:block;margin:0 0 .7em 0;overflow:hidden;}
#wiki-wrapper #gollum-editor .singleline input{background:#fff;border:1px solid #ddd;color:#000;font-size:1.3em;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;line-height:1.8em;margin:1em 0 .4em;padding:.5em;width:883px;}
#wiki-wrapper #gollum-editor .singleline input.ph{color:#999;}
#wiki-wrapper #gollum-editor-title-field input#gollum-editor-page-title{font-weight:bold;margin-top:0;}
#wiki-wrapper #gollum-editor-title-field.active{border-bottom:1px solid #ddd;display:block;margin:0 0 .3em 0;padding:0 0 .5em 0;}
#wiki-wrapper #gollum-editor-title-field input#gollum-editor-page-title.ph{color:#000;}
#wiki-wrapper #gollum-editor #gollum-editor-type-switcher{display:none;}
#wiki-wrapper #gollum-editor #gollum-editor-function-bar{border-bottom:1px solid #ddd;overflow:hidden;padding:0;}
#wiki-wrapper #gollum-editor-title-field+#gollum-editor-function-bar{margin-top:.6em;}
#wiki-wrapper #gollum-editor #gollum-editor-function-bar #gollum-editor-function-buttons{display:none;}
#wiki-wrapper #gollum-editor #gollum-editor-function-bar.active #gollum-editor-function-buttons{display:block;float:left;overflow:hidden;padding:0 0 1.1em 0;}
#wiki-wrapper #gollum-editor #gollum-editor-function-bar a.function-button{background:#f7f7f7;border:1px solid #ddd;color:#333;display:block;float:left;height:25px;overflow:hidden;margin:.2em .5em 0 0;text-shadow:0 1px 0 #fff;width:25px;border-radius:.3em;-moz-border-radius:.3em;-webkit-border-radius:.3em;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#f4f4f4),to(#ececec));background:-moz-linear-gradient(top,#f4f4f4,#ececec);}
#wiki-wrapper #gollum-editor #gollum-editor-function-bar a.function-button:hover{color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,0.3);text-decoration:none;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#599bdc',endColorstr='#3072b3');background:-webkit-gradient(linear,left top,left bottom,from(#599bdc),to(#3072b3));background:-moz-linear-gradient(top,#599bdc,#3072b3);}
#wiki-wrapper #gollum-editor #gollum-editor-function-bar a span{background-image:url(/images/modules/wiki/icon-sprite.png?v2);background-repeat:no-repeat;display:block;height:25px;overflow:hidden;text-indent:-5000px;width:25px;}
#wiki-wrapper a#function-bold span{background-position:0 0;}
#wiki-wrapper a#function-italic span{background-position:-27px 0;}
#wiki-wrapper a#function-underline span{background-position:-54px 0;}
#wiki-wrapper a#function-code span{background-position:-82px 0;}
#wiki-wrapper a#function-ul span{background-position:-109px 0;}
#wiki-wrapper a#function-ol span{background-position:-136px 0;}
#wiki-wrapper a#function-blockquote span{background-position:-163px 0;}
#wiki-wrapper a#function-hr span{background-position:-190px 0;}
#wiki-wrapper a#function-h1 span{background-position:-217px 0;}
#wiki-wrapper a#function-h2 span{background-position:-244px 0;}
#wiki-wrapper a#function-h3 span{background-position:-271px 0;}
#wiki-wrapper a#function-internal-link span{background-position:-298px 0;}
#wiki-wrapper a#function-image span{background-position:-324px 0;}
#wiki-wrapper a#function-help span{background-position:-405px 0;}
#wiki-wrapper a#function-link span{background-position:-458px 0;}
#wiki-wrapper a#function-bold:hover span{background-position:0 -28px;}
#wiki-wrapper a#function-italic:hover span{background-position:-27px -28px;}
#wiki-wrapper a#function-underline:hover span{background-position:-54px -28px;}
#wiki-wrapper a#function-code:hover span{background-position:-82px -28px;}
#wiki-wrapper a#function-ul:hover span{background-position:-109px -28px;}
#wiki-wrapper a#function-ol:hover span{background-position:-136px -28px;}
#wiki-wrapper a#function-blockquote:hover span{background-position:-163px -28px;}
#wiki-wrapper a#function-hr:hover span{background-position:-190px -28px;}
#wiki-wrapper a#function-h1:hover span{background-position:-217px -28px;}
#wiki-wrapper a#function-h2:hover span{background-position:-244px -28px;}
#wiki-wrapper a#function-h3:hover span{background-position:-271px -28px;}
#wiki-wrapper a#function-internal-link:hover span{background-position:-298px -28px;}
#wiki-wrapper a#function-image:hover span{background-position:-324px -28px;}
#wiki-wrapper a#function-help:hover span{background-position:-405px -28px;}
#wiki-wrapper a#function-link:hover span{background-position:-458px -28px;}
#wiki-wrapper #gollum-editor #gollum-editor-function-bar a.disabled{display:none;}
#wiki-wrapper #gollum-editor #gollum-editor-function-bar span.function-divider{display:block;float:left;width:.5em;}
#wiki-wrapper #gollum-editor #gollum-editor-function-bar #gollum-editor-format-selector{overflow:hidden;padding:0 0 1.1em 0;}
#gollum-editor #gollum-editor-function-bar #gollum-editor-format-selector select{background-color:#f9f9f9;border:1px solid #f9f9f9;float:right;font-size:1.1em;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:bold;line-height:1.6em;padding:.5em .7em;margin-bottom:0;-moz-outline:none;}
#gollum-editor #gollum-editor-function-bar #gollum-editor-format-selector select:hover{background-color:#fff;border:1px solid #ddd;border-radius:.5em;-moz-border-radius:.5em;-webkit-border-radius:.5em;-moz-outline:none;}
#gollum-editor #gollum-editor-function-bar #gollum-editor-format-selector label{color:#999;float:right;font-size:1.1em;font-weight:bold;line-height:1.6em;padding:.6em .5em 0 0;}
#gollum-editor #gollum-editor-function-bar #gollum-editor-format-selector label:after{content:':';}
.osx.webkit #gollum-editor #gollum-editor-function-bar #gollum-editor-format-selector select{margin-top:.6em;}
#wiki-wrapper #gollum-editor textarea#gollum-editor-body{background:#fff;border:1px solid #ddd;font-size:1.3em;font-family:Consolas,Monaco,"DejaVu Sans Mono","Bitstream Vera Sans Mono","Courier New",monospace;line-height:1.7em;margin:1em 0 .4em;padding:.5em;width:883px;height:30em;}
#wiki-wrapper #gollum-editor input#gollum-editor-submit{background-color:#f7f7f7;border:1px solid #d4d4d4;color:#333;cursor:pointer;display:block;float:left;font-size:1.2em;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:bold;margin:0;padding:.4em 1em;text-shadow:0 1px 0 #fff;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#f4f4f4),to(#ececec));background:-moz-linear-gradient(top,#f4f4f4,#ececec);border-radius:3px;-moz-border-radius:3px;-webkit-border-radius:3px;}
.webkit #wiki-wrapper #gollum-editor input#gollum-editor-submit{padding:.45em 1em .45em;}
.ie #wiki-wrapper #gollum-editor input#gollum-editor-submit{padding:.4em 1em .5em;}
#wiki-wrapper #gollum-editor input#gollum-editor-submit:hover{background:#3072b3;border-color:#518cc6 #518cc6 #2a65a0;color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,0.3);text-decoration:none;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#599bdc',endColorstr='#3072b3');background:-webkit-gradient(linear,left top,left bottom,from(#599bdc),to(#3072b3));background:-moz-linear-gradient(top,#599bdc,#3072b3);}
#wiki-wrapper #gollum-editor .collapsed,#wiki-wrapper #gollum-editor .expanded{border-bottom:1px solid #ddd;display:block;overflow:hidden;padding:1em 0 .5em;}
#wiki-wrapper #gollum-editor #gollum-editor-body+.collapsed,#wiki-wrapper #gollum-editor #gollum-editor-body+.expanded{border-top:1px solid #ddd;margin-top:.7em;}
#wiki-wrapper #gollum-editor .collapsed a.button,#wiki-wrapper #gollum-editor .expanded a.button{background:#f7f7f7;border:1px solid #ddd;color:#333;display:block;float:left;height:25px;overflow:hidden;margin:.2em .5em .75em 0;padding:0;text-shadow:0 1px 0 #fff;width:25px;border-radius:.3em;-moz-border-radius:.3em;-webkit-border-radius:.3em;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#f4f4f4),to(#ececec));background:-moz-linear-gradient(top,#f4f4f4,#ececec);}
#wiki-wrapper #gollum-editor .collapsed h4,#wiki-wrapper #gollum-editor .expanded h4{font-size:1.6em;float:left;margin:0;padding:.4em 0 0 .3em;text-shadow:0 -1px 0 #fff;}
#wiki-wrapper #gollum-editor .collapsed a.button:hover,#wiki-wrapper #gollum-editor .expanded h4 a.button:hover{color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,0.3);text-decoration:none;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#599bdc',endColorstr='#3072b3');background:-webkit-gradient(linear,left top,left bottom,from(#599bdc),to(#3072b3));background:-moz-linear-gradient(top,#599bdc,#3072b3);}
#wiki-wrapper #gollum-editor .collapsed a span,#wiki-wrapper #gollum-editor .expanded a span{background-image:url(/images/modules/wiki/icon-sprite.png);background-position:-351px -1px;background-repeat:no-repeat;display:block;height:25px;overflow:hidden;text-indent:-5000px;width:25px;}
#wiki-wrapper #gollum-editor .collapsed a:hover span{background-position:-351px -28px;}
#wiki-wrapper #gollum-editor .expanded a span{background-position:-378px 0;}
#wiki-wrapper #gollum-editor .expanded a:hover span{background-position:-378px -28px;}
#wiki-wrapper #gollum-editor .collapsed textarea{display:none;}
#wiki-wrapper #gollum-editor .expanded textarea{border:1px solid #ddd;clear:both;display:block;font-size:1.2em;font-family:Consolas,Monaco,"DejaVu Sans Mono","Bitstream Vera Sans Mono","Courier New",monospace;height:7em;line-height:1.7em;margin:.7em 0;padding:.5em;width:883px;}
#wiki-wrapper #gollum-editor a.gollum-minibutton,#wiki-wrapper #gollum-editor a.gollum-minibutton:visited{background-color:#f7f7f7;border:1px solid #d4d4d4;color:#333;cursor:pointer;display:block;font-size:1.2em;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:bold;line-height:1.2em;margin:0 0 0 .8em;padding:.5em 1em;text-shadow:0 1px 0 #fff;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#f4f4f4),to(#ececec));background:-moz-linear-gradient(top,#f4f4f4,#ececec);border-radius:3px;-moz-border-radius:3px;-webkit-border-radius:3px;}
#wiki-wrapper #gollum-editor a.gollum-minibutton:hover{background:#3072b3;border-color:#518cc6 #518cc6 #2a65a0;color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,0.3);text-decoration:none;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#599bdc',endColorstr='#3072b3');background:-webkit-gradient(linear,left top,left bottom,from(#599bdc),to(#3072b3));background:-moz-linear-gradient(top,#599bdc,#3072b3);}
#wiki-wrapper #gollum-editor #gollum-editor-preview{float:left;font-weight:normal;padding:left;}
#wiki-wrapper #gollum-editor-help{margin:0;overflow:hidden;padding:0;border:1px solid #ddd;border-width:0 1px 1px 1px;}
#wiki-wrapper #gollum-editor-help-parent,#wiki-wrapper #gollum-editor-help-list{display:block;float:left;height:17em;list-style-type:none;overflow:auto;margin:0;padding:1em 0;width:160px;}
#wiki-wrapper #gollum-editor-help-parent{border-right:1px solid #eee;}
#wiki-wrapper #gollum-editor-help-list{background:#fafafa;border-right:1px solid #eee;}
#wiki-wrapper #gollum-editor-help-parent li,#wiki-wrapper #gollum-editor-help-list li{font-size:1.2em;line-height:1.6em;margin:0;padding:0;}
#wiki-wrapper #gollum-editor-help-parent li a,#wiki-wrapper #gollum-editor-help-list li a{border:1px solid transparent;border-width:1px 0;display:block;font-weight:bold;height:100%;width:auto;padding:.2em 1em;text-shadow:0 -1px 0 #fff;}
#wiki-wrapper #gollum-editor-help-parent li a:hover,#wiki-wrapper #gollum-editor-help-list li a:hover{background:#fff;border-color:#f0f0f0;text-decoration:none;box-shadow:none;}
#wiki-wrapper #gollum-editor-help-parent li a.selected,#wiki-wrapper #gollum-editor-help-list li a.selected{border:1px solid #eee;border-bottom-color:#e7e7e7;border-width:1px 0;background:#fff;color:#000;box-shadow:0 1px 2px #f0f0f0;}
#wiki-wrapper #gollum-editor-help-wrapper{background:#fff;overflow:auto;height:17em;padding:1em;}
#wiki-wrapper #gollum-editor-help-content{font-size:1.2em;margin:0 1em 0 .5em;padding:0;line-height:1.8em;}
#wiki-wrapper #gollum-editor-help-content p{margin:0 0 1em 0;padding:0;}
#wiki-wrapper .ie #gollum-editor .singleline input{padding-top:.25em;padding-bottom:.75em;}
#wiki-wrapper #template{font-size:14px;line-height:23px!important;margin-bottom:40px;}
#wiki-wrapper #template a.absent{color:#c00;}
#wiki-wrapper #template p{margin:16px 0 0;padding:0;}
#wiki-wrapper #template * li p.first{display:inline-block;}
#wiki-wrapper #template h1,#wiki-wrapper #template h2,#wiki-wrapper #template h3,#wiki-wrapper #template h4,#wiki-wrapper #template h5,#wiki-wrapper #template h6{margin:0;padding:0;}
#wiki-wrapper #template h1{border-top:4px solid #ccc;font-size:32px;line-height:normal;padding:10px 0 0;margin:30px 0 0;}
#wiki-wrapper #template h2{border-top:4px solid #ccc;font-size:22px;line-height:normal;margin:22px 0 0;padding:7px 0 0;}
#wiki-wrapper #template h3{font-size:16px;line-height:26px;padding:26px 0 0;}
#wiki-wrapper #template h4{font-size:14px;line-height:26px;padding:18px 0 4px;font-weight:bold;text-transform:uppercase;}
#wiki-wrapper #template h5{font-size:13px;line-height:26px;padding:14px 0 0;font-weight:bold;text-transform:uppercase;}
#wiki-wrapper #template h6{color:#666;font-size:14px;line-height:26px;padding:18px 0 0;font-weight:normal;font-variant:italic;}
#wiki-wrapper #template hr{background-color:#ccc;color:#ccc;border:2px solid #ccc;margin:20px 0;padding:0;}
#wiki-wrapper #template>h2:first-child,#wiki-wrapper #template>h1:first-child,#wiki-wrapper #template>h1:first-child+h2{border:0;margin:12px 0 0;padding:10px 0 0;}
#wiki-wrapper #template>h3:first-child,#wiki-wrapper #template>h4:first-child,#wiki-wrapper #template>h5:first-child,#wiki-wrapper #template>h6:first-child{margin:13px 0 0 0;padding:0;}
#wiki-wrapper #template>h1:first-child,#wiki-wrapper .gollum-rest-content #template>div:first-child>div:first-child>h1:first-child,#wiki-wrapper .gollum-pod-content #template>a.dummyTopAnchor:first-child+h1,#wiki-wrapper .gollum-org-content #template>p.title:first-child,#wiki-wrapper .gollum-asciidoc-content #template>div#header:first-child>h1:first-child{display:none;}
#wiki-wrapper #template h4+p,#wiki-wrapper #template h5+p,#wiki-wrapper #template h6+p{margin-top:0;}
#wiki-wrapper #template ul,#wiki-wrapper #template ol{margin:0 0 0 1.5em;padding:20px 0 0;}
#wiki-wrapper #template ul li ul,#wiki-wrapper #template ol li ol,#wiki-wrapper #template ul li ol,#wiki-wrapper #template ol li ul,#wiki-wrapper #template ul ul,#wiki-wrapper #template ol ol{padding:0 0 0 14px;}
#wiki-wrapper #template dl{margin:0;padding:20px 0 0;}
#wiki-wrapper #template dl dt{font-size:14px;font-weight:bold;line-height:normal;margin:0;padding:20px 0 0;}
#wiki-wrapper #template dl dt:first-child{padding:0;}
#wiki-wrapper #template dl dd{font-size:13px;margin:0;padding:3px 0 0;}
#wiki-wrapper #template blockquote{margin:1em 0;border-left:4px solid #ddd;padding-left:.8em;color:#555;}
#wiki-wrapper #template table{border-collapse:collapse;margin:20px 0 0;padding:0;}
#wiki-wrapper #template table * tr{border-top:1px solid #ccc;background-color:#fff;margin:0;padding:0;}
#wiki-wrapper #template table * tr:nth-child(2n){background-color:#f8f8f8;}
#wiki-wrapper #template table * tr th,#wiki-wrapper #template table * tr td{border:1px solid #ccc;text-align:left;margin:0;padding:6px 13px;}
#wiki-wrapper #template img{max-width:100%;}
#wiki-wrapper #template span.frame{display:block;overflow:hidden;}
#wiki-wrapper #template span.frame>span{border:1px solid #ddd;display:block;float:left;overflow:hidden;margin:13px 0 0;padding:7px;width:auto;}
#wiki-wrapper #template span.frame span img{display:block;float:left;}
#wiki-wrapper #template span.frame span span{clear:both;color:#333;display:block;padding:5px 0 0;}
#wiki-wrapper #template span.align-center{display:block;overflow:hidden;clear:both;}
#wiki-wrapper #template span.align-center>span{display:block;overflow:hidden;margin:13px auto 0;text-align:center;}
#wiki-wrapper #template span.align-center span img{margin:0 auto;text-align:center;}
#wiki-wrapper #template span.align-right{display:block;overflow:hidden;clear:both;}
#wiki-wrapper #template span.align-right>span{display:block;overflow:hidden;margin:13px 0 0;text-align:right;}
#wiki-wrapper #template span.align-right span img{margin:0;text-align:right;}
#wiki-wrapper #template span.float-left{display:block;margin-right:13px;overflow:hidden;float:left;}
#wiki-wrapper #template span.float-left span{margin:13px 0 0;}
#wiki-wrapper #template span.float-right{display:block;margin-left:13px;overflow:hidden;float:right;}
#wiki-wrapper #template span.float-right>span{display:block;overflow:hidden;margin:13px auto 0;text-align:right;}
#wiki-wrapper #template code,#wiki-wrapper #template tt{background-color:#f8f8f8;border:1px solid #dedede;font-size:13px;padding:0;-moz-border-radius:3px;-webkit-border-radius:3px;border-radius:3px;}
#wiki-wrapper #template .highlight pre,#wiki-wrapper #template pre{background-color:#f8f8f8;border:1px solid #ccc;font-size:13px;line-height:19px;overflow:auto;padding:6px 10px;-moz-border-radius:3px;-webkit-border-radius:3px;border-radius:3px;}
#wiki-wrapper #template>pre,#wiki-wrapper #template>div.highlight{margin:20px 0 0;}
#wiki-wrapper #template pre code,#wiki-wrapper #template pre tt{background-color:transparent;border:none;}
#wiki-wrapper #template .highlight{background:#fff;}
#wiki-wrapper #template .highlight .c{color:#998;font-style:italic;}
#wiki-wrapper #template .highlight .err{color:#a61717;background-color:#e3d2d2;}
#wiki-wrapper #template .highlight .k{font-weight:bold;}
#wiki-wrapper #template .highlight .o{font-weight:bold;}
#wiki-wrapper #template .highlight .cm{color:#998;font-style:italic;}
#wiki-wrapper #template .highlight .cp{color:#999;font-weight:bold;}
#wiki-wrapper #template .highlight .c1{color:#998;font-style:italic;}
#wiki-wrapper #template .highlight .cs{color:#999;font-weight:bold;font-style:italic;}
#wiki-wrapper #template .highlight .gd{color:#000;background-color:#fdd;}
#wiki-wrapper #template .highlight .gd .x{color:#000;background-color:#faa;}
#wiki-wrapper #template .highlight .ge{font-style:italic;}
#wiki-wrapper #template .highlight .gr{color:#a00;}
#wiki-wrapper #template .highlight .gh{color:#999;}
#wiki-wrapper #template .highlight .gi{color:#000;background-color:#dfd;}
#wiki-wrapper #template .highlight .gi .x{color:#000;background-color:#afa;}
#wiki-wrapper #template .highlight .gc{color:#999;background-color:#EAF2F5;}
#wiki-wrapper #template .highlight .go{color:#888;}
#wiki-wrapper #template .highlight .gp{color:#555;}
#wiki-wrapper #template .highlight .gs{font-weight:bold;}
#wiki-wrapper #template .highlight .gu{color:#aaa;}
#wiki-wrapper #template .highlight .gt{color:#a00;}
#guides.wiki-git-access #head{border-bottom:1px solid #ccc;margin:14px 0 5px;padding:0 0 .5em 0;overflow:hidden;}
#guides.wiki-git-access h1{color:#999;font-size:33px;font-weight:normal;float:left;line-height:normal;margin:0;padding:0;}
.wiki-git-access #url_box{margin-top:14px;}
#gollum-dialog-dialog h4{border-bottom:1px solid #ddd;color:#333;font-size:16px;line-height:normal;font-weight:bold;margin:0 0 .75em 0;padding:0 0 .4em;text-shadow:0 -1px 0 #f7f7f7;}
#gollum-dialog-dialog-body{font-size:12px;line-height:16px;margin:0;padding:0;}
#gollum-dialog-dialog-body fieldset{display:block;border:0;margin:0;overflow:hidden;padding:0 1em;}
#gollum-dialog-dialog-body fieldset .field{margin:0 0 1.5em 0;padding:0;}
#gollum-dialog-dialog-body fieldset .field label{color:#666;display:block;font-size:1.2em;font-weight:bold;line-height:1.6em;margin:0;padding:0;min-width:80px;}
#gollum-dialog-dialog-body fieldset .field input[type="text"]{border:1px solid #ccc;display:block;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:12px;line-height:16px;margin:.3em 0 0 0;padding:.3em .5em;width:96.5%;}
#gollum-dialog-dialog-body fieldset .field input.code{font-family:'Monaco','Courier New',Courier,monospace;}
#gollum-dialog-dialog-body fieldset .field:last-child{margin:0 0 1em 0;}
#gollum-dialog-dialog-buttons{border-top:1px solid #ddd;overflow:hidden;margin:1.2em 0 0 0;padding:1em 0 0;}
#gollum-dialog-dialog a.gollum-minibutton{float:right;margin-right:.5em;width:auto;}
#gollum-dialog-dialog a.gollum-minibutton,#gollum-dialog-dialog a.gollum-minibutton:visited{background-color:#f7f7f7;border:1px solid #d4d4d4;color:#333;cursor:pointer;display:inline;font-size:12px;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-weight:bold;margin:0 0 0 .8em;padding:.4em 1em;text-shadow:0 1px 0 #fff;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#f4f4f4',endColorstr='#ececec');background:-webkit-gradient(linear,left top,left bottom,from(#f4f4f4),to(#ececec));background:-moz-linear-gradient(top,#f4f4f4,#ececec);border-radius:3px;-moz-border-radius:3px;-webkit-border-radius:3px;}
#gollum-dialog-dialog a.gollum-minibutton:hover{background:#3072b3;border-color:#518cc6 #518cc6 #2a65a0;color:#fff;text-shadow:0 -1px 0 rgba(0,0,0,0.3);text-decoration:none;filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#599bdc',endColorstr='#3072b3');background:-webkit-gradient(linear,left top,left bottom,from(#599bdc),to(#3072b3));background:-moz-linear-gradient(top,#599bdc,#3072b3);}
#wiki-wrapper #files .file .data tr td.line_numbers{width:1%;font-size:12px;}
#wiki-wrapper .featurelike h1{color:#fff;font-size:16px;font-weight:bold;background-color:#405a6a;background:-moz-linear-gradient(center top,'#829AA8','#405A6A');filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr='#829aa8',endColorstr='#405a6a');background:-webkit-gradient(linear,left top,left bottom,from(#829aa8),to(#405a6a));background:-moz-linear-gradient(top,#829aa8,#405a6a);border:1px solid #677c89;border-bottom-color:#6b808d;border-radius:3px 3px 0 0;-moz-border-radius:3px 3px 0 0;-webkit-border-radius:3px 3px 0 0;text-shadow:0 -1px 0 rgba(0,0,0,0.7);margin:0;padding:8px 18px;}
#wiki-wrapper .featurelike .featurebody{background-color:#e9f1f4;overflow:hidden;border-style:solid;border-width:1px 1px 2px;border-color:#e9f1f4 #d8dee2 #d8dee2;border-radius:0 0 3px 3px;-moz-border-radius:0 0 3px 3px;-webkit-border-radius:0 0 3px 3px;}
#wiki-wrapper .featurelike .featurebody img{float:left;margin:18px 18px 20px;}
#wiki-wrapper .featurelike .featurebody .feature-description{float:left;margin:57px 0 0 0;padding:0;width:300px;}
#wiki-wrapper .featurelike .featurebody .feature-description h3,#wiki-wrapper .featurelike .featurebody .creating-wiki h3{color:#2f424e;font-size:18px;font-weight:normal;margin:0 0 .5em;text-shadow:0 -1px 0 rgba(100,100,100,0.1);}
#wiki-wrapper .featurelike .featurebody .feature-description p,#wiki-wrapper .featurelike .featurebody .creating-wiki p{color:#2f424e;font-size:14px;font-weight:normal;margin:0 0 1em;text-shadow:0 -1px 0 rgba(100,100,100,0.1);}
#wiki-wrapper .featurelike .featurebody .feature-description button{margin:0 8px 0 0;}
#wiki-wrapper .featurelike .featurebody .feature-description span#go-back{font-size:14px;font-weight:normal;position:relative;text-shadow:0 -1px 0 rgba(100,100,100,0.1);top:1px;}
#wiki-wrapper .featurelike .featurebody .creating-wiki{text-align:center;padding:20px 18px;}
#wiki-wrapper .featurelike .featurebody .creating-wiki h3{background:transparent url(/images/modules/wiki/loading_indicator.gif) center top no-repeat;padding-top:30px;margin-top:10px;}
.ie #head #searchbar #searchbar-fauxtext input#search-query{border:0;float:left;padding:.4em 0 0 .5em;}
.ie #head #searchbar #searchbar-fauxtext #search-submit span{height:2.25em;}
.ie7 #head #searchbar,.ie7 #head ul.actions{margin:1em 0 0 0;}
.ie7 ul.actions{margin-left:0;}
.ie7 .compare #footer ul.actions{margin-top:1em;}
.ie7 .compare div.data{overflow:auto;}
.ie7 .history #version-form{margin:-0.5em 0 -0.5em!important;}
.ie7 #gollum-editor{padding-bottom:0;}
.ie7 #gollum-editor-help-parent li a,.ie7 #gollum-editor-help-list li a{height:auto;}
.ie7 #gollum-editor #gollum-editor-format-selector{margin-top:6px;}
.ie7 #gollum-editor .singleline input{padding-top:.25em;}
.ie7 #gollum-editor .collapsed{padding-bottom:1.1em;}
.ie7 #gollum-editor #gollum-editor-submit{padding:.5em 1em .3em!important;}
.ie7 #gollum-editor #gollum-editor-preview{line-height:1.3em;}
.ie7 #gollum-editor form{margin:0;}
.ie7 #gollum-editor #gollum-editor-format-selector label{padding-top:.1em!important;}
.ie7 #wiki-wrapper .featurelike #wiki-create-prompt{padding-bottom:20px;}
.wikistyle h1,.wikistyle h2,.wikistyle h3,.wikistyle h4,.wikistyle h5,.wikistyle h6{border:0!important;}
.wikistyle h1{font-size:170%!important;border-top:4px solid #aaa!important;padding-top:.5em!important;margin-top:1.5em!important;}
.wikistyle h1:first-child{margin-top:0!important;padding-top:.25em!important;border-top:none!important;}
.wikistyle h2{font-size:150%!important;margin-top:1.5em!important;border-top:4px solid #e0e0e0!important;padding-top:.5em!important;}
.wikistyle h3{margin-top:1em!important;}
.wikistyle hr{border:1px solid #ddd;}
.wikistyle p{margin:1em 0!important;line-height:1.5em!important;}
.wikistyle a.absent{color:#a00;}
.wikistyle ul,#wiki-form .content-body ul{margin:1em 0 1em 2em!important;}
.wikistyle ol,#wiki-form .content-body ol{margin:1em 0 1em 2em!important;}
.wikistyle ul li,#wiki-form .content-body ul li,.wikistyle ol li,#wiki-form .content-body ol li{margin-top:.5em;margin-bottom:.5em;}
.wikistyle ul ul,.wikistyle ul ol,.wikistyle ol ol,.wikistyle ol ul,#wiki-form .content-body ul ul,#wiki-form .content-body ul ol,#wiki-form .content-body ol ol,#wiki-form .content-body ol ul{margin-top:0!important;margin-bottom:0!important;}
.wikistyle blockquote{margin:1em 0!important;border-left:5px solid #ddd!important;padding-left:.6em!important;color:#555!important;}
.wikistyle dt{font-weight:bold!important;margin-left:1em!important;}
.wikistyle dd{margin-left:2em!important;margin-bottom:1em!important;}
.wikistyle table{margin:1em 0!important;}
.wikistyle table th{border-bottom:1px solid #bbb!important;padding:.2em 1em!important;}
.wikistyle table td{border-bottom:1px solid #ddd!important;padding:.2em 1em!important;}
.wikistyle pre{margin:1em 0;font-size:12px;background-color:#eee;border:1px solid #ddd;padding:5px;line-height:1.5em;color:#444;overflow:auto;-webkit-box-shadow:rgba(0,0,0,0.07) 0 1px 2px inset;-webkit-border-radius:3px;-moz-border-radius:3px;border-radius:3px;}
.wikistyle pre::-webkit-scrollbar{height:8px;width:8px;}
.wikistyle pre::-webkit-scrollbar-track-piece{margin-bottom:10px;background-color:#e5e5e5;border-bottom-left-radius:4px 4px;border-bottom-right-radius:4px 4px;border-top-left-radius:4px 4px;border-top-right-radius:4px 4px;}
.wikistyle pre::-webkit-scrollbar-thumb:vertical{height:25px;background-color:#ccc;-webkit-border-radius:4px;-webkit-box-shadow:0 1px 1px rgba(255,255,255,1);}
.wikistyle pre::-webkit-scrollbar-thumb:horizontal{width:25px;background-color:#ccc;-webkit-border-radius:4px;}
.wikistyle pre code{padding:0!important;font-size:12px!important;background-color:#eee!important;border:none!important;}
.wikistyle code{font-size:12px!important;background-color:#f8f8ff!important;color:#444!important;padding:0 .2em!important;border:1px solid #dedede!important;}
.wikistyle a code,.wikistyle a:link code,.wikistyle a:visited code{color:#4183c4!important;}
.wikistyle img{max-width:100%;}
.wikistyle pre.console{margin:1em 0!important;font-size:12px!important;background-color:black!important;padding:.5em!important;line-height:1.5em!important;color:white!important;}
.wikistyle pre.console code{padding:0!important;font-size:12px!important;background-color:black!important;border:none!important;color:white!important;}
.wikistyle pre.console span{color:#888!important;}
.wikistyle pre.console span.command{color:yellow!important;}
.wikistyle .frame{margin:0;display:inline-block;}
.wikistyle .frame img{display:block;}
.wikistyle .frame>span{display:block;border:1px solid #aaa;padding:4px;}
.wikistyle .frame span span{display:block;font-size:10pt;margin:0;padding:4px 0 2px 0;text-align:center;line-height:10pt;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;}
.wikistyle .float-left{float:left;padding:.5em 1em .25em 0;}
.wikistyle .float-right{float:right;padding:.5em 0 .25em 1em;}
.wikistyle .align-left{display:block;text-align:left;}
.wikistyle .align-center{display:block;text-align:center;}
.wikistyle .align-right{display:block;text-align:right;}
""")

def main():
    httpd = BaseHTTPServer.HTTPServer(('', 8055), H)
    print "Serving %s - Listeting on http://localhost:8055/" % sys.argv[1]
    httpd.serve_forever()

if __name__ == '__main__':
    main()

import re

with open('dashboard/templates/dashboard/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# find toolbar
toolbar_start = html.find('<!-- Toolbar -->')
grid_start = html.find('<!-- Fan unit grid -->')

# find loop
loop_start = html.find('{% for unit in units %}', grid_start)
empty_start = html.find('{% empty %}', loop_start)
endfor_start = html.find('{% endfor %}', empty_start)
grid_end = html.find('</div>', endfor_start) + 6

card_template = html[loop_start + len('{% for unit in units %}'):empty_start].strip()
empty_template = html[empty_start:grid_end].strip()

new_html_block = '''
<!-- CSS for Zone Accordion -->
<style>
.zone-accordion {
  margin-bottom: 16px;
  border: 1px solid var(--border);
  border-radius: 14px;
  background: var(--bg-surface);
  overflow: hidden;
}
.zone-header {
  padding: 14px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  background: var(--bg-surface);
  transition: background 0.2s;
}
.zone-header:hover {
  background: var(--bg-hover);
}
.zone-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--txt);
  display: flex;
  align-items: center;
  gap: 8px;
}
.zone-toggle-icon {
  font-size: 14px;
  transition: transform 0.3s;
  color: var(--txt-2);
}
.zone-accordion.expanded .zone-toggle-icon {
  transform: rotate(180deg);
}
.zone-content {
  padding: 16px;
  border-top: 1px solid var(--border);
  display: none;
}
.zone-accordion.expanded .zone-content {
  display: block;
}
</style>

<!-- Zone Accordions -->
<div class="zones-container">
  {% for z in zones %}
  <div class="zone-accordion expanded" id="acc-{{ forloop.counter }}">
    <div class="zone-header" onclick="document.getElementById('acc-{{ forloop.counter }}').classList.toggle('expanded')">
      <div class="zone-title">
        📍 Khu vực: {{ z }}
      </div>
      <div class="zone-toggle-icon">▼</div>
    </div>
    <div class="zone-content">
      <div class="unit-grid">
        {% for unit in units %}
          {% if unit.zone == z %}
            ''' + card_template.replace('\n', '\n            ') + '''
          {% endif %}
        {% endfor %}
      </div>
    </div>
  </div>
  {% empty %}
    ''' + empty_template.replace('\n', '\n    ') + '''
</div>
'''

final_html = html[:toolbar_start] + new_html_block + html[grid_end:]

with open('dashboard/templates/dashboard/home.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

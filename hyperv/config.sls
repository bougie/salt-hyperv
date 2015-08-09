{% from "hyperv/default.yml" import rawmap with context %}
{% set rawmap = salt['pillar.get']('hyperv', rawmap, merge=True) %}

{% if rawmap.netadapters is defined %}
    {% for tgt, props in rawmap.netadapters.items() %}
{{tgt ~ '_netadapter'}}:
    hyperv_netadapter.managed:
        - tgt: {{tgt}}
        {% for prop_name, prop_value in props.items() %}
        - {{prop_name}}: {{prop_value}}
        {% endfor %}
    {% endfor %}
{% endif %}

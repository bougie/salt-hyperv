{% from "hyperv/default.yml" import rawmap with context %}
{% set rawmap = salt['pillar.get']('hyperv', rawmap) %}

hyperv_pkg:
    win_servermanager.installed:
        - name: Hyper-V

hyperv_ps_pkg:
    win_servermanager.installed:
        - name: Hyper-V-Powershell

{% if rawmap.with_gui is defined and rawmap.with_gui %}
hyperv_gui_pkg:
    win_servermanager.installed:
        - name: Hyper-V-Tools
{% endif %}

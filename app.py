import streamlit as st
import dns.resolver
import dns.exception
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Optional
import plotly.graph_objects as go
import plotly.express as px

# DNS 服务器配置
DNS_SERVERS = {
    '阿里 DNS': '223.5.5.5',
    'Google DNS': '8.8.8.8'
}

# 记录类型
RECORD_TYPES = ['A', 'AAAA']

class DNSBenchmark:
    def __init__(self):
        self.results = {}

    def query_dns(self, domain: str, dns_server: str, record_type: str) -> Tuple[List[str], float, Optional[int]]:
        """
        查询 DNS 记录并返回结果、耗时和 TTL
        """
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        resolver.timeout = 5
        resolver.lifetime = 10

        start_time = time.time()
        try:
            answers = resolver.resolve(domain, record_type)
            elapsed_time = time.time() - start_time

            # 获取记录值和 TTL
            records = []
            ttl = None
            for rdata in answers:
                records.append(str(rdata))
                if ttl is None:
                    ttl = answers.ttl

            return records, elapsed_time * 1000, ttl  # 转换为毫秒

        except (dns.exception.Timeout, dns.exception.DNSException) as e:
            elapsed_time = time.time() - start_time
            return [], elapsed_time * 1000, None

    def benchmark_domain(self, domain: str) -> Dict:
        """
        对指定域名进行 DNS 基准测试
        """
        results = {}

        for dns_name, dns_server in DNS_SERVERS.items():
            results[dns_name] = {}

            for record_type in RECORD_TYPES:
                records, latency, ttl = self.query_dns(domain, dns_server, record_type)
                results[dns_name][record_type] = {
                    'records': records,
                    'latency_ms': latency,
                    'ttl': ttl
                }

        return results

def create_latency_chart(results: Dict) -> go.Figure:
    """
    创建解析耗时对比图表
    """
    dns_servers = list(results.keys())
    record_types = ['A', 'AAAA']

    fig = go.Figure()

    for i, record_type in enumerate(record_types):
        latencies = []
        labels = []

        for dns_server in dns_servers:
            latency = results[dns_server][record_type]['latency_ms']
            latencies.append(latency)
            labels.append(f"{dns_server}\n{record_type}")

        # 为不同记录类型使用不同的颜色
        colors = ['#1f77b4', '#ff7f0e']  # 蓝色和橙色

        fig.add_trace(go.Bar(
            name=record_type,
            x=labels,
            y=latencies,
            marker_color=colors[i],
            text=[f"{lat:.1f}ms" for lat in latencies],
            textposition='auto',
        ))

    fig.update_layout(
        title="DNS 解析耗时对比 (毫秒)",
        xaxis_title="DNS 服务器和记录类型",
        yaxis_title="耗时 (ms)",
        barmode='group',
        height=400
    )

    return fig

def display_results(results: Dict, domain: str):
    """
    在 Streamlit 中展示测试结果
    """
    st.subheader("📊 测试结果")

    # 创建两列来展示不同 DNS 服务器的结果
    cols = st.columns(2)

    for i, (dns_name, dns_data) in enumerate(results.items()):
        with cols[i]:
            st.markdown(f"### {dns_name}")

            # IPv4 (A 记录)
            if dns_data['A']['records']:
                st.markdown("**IPv4 (A 记录):**")
                for record in dns_data['A']['records']:
                    st.success(f"✓ {record}")
                st.info(f"耗时: {dns_data['A']['latency_ms']:.1f}ms")
                if dns_data['A']['ttl']:
                    st.info(f"TTL: {dns_data['A']['ttl']}s")
            else:
                st.error("❌ IPv4 解析失败")

            st.markdown("---")

            # IPv6 (AAAA 记录)
            if dns_data['AAAA']['records']:
                st.markdown("**IPv6 (AAAA 记录):**")
                for record in dns_data['AAAA']['records']:
                    st.success(f"✓ {record}")
                st.info(f"耗时: {dns_data['AAAA']['latency_ms']:.1f}ms")
                if dns_data['AAAA']['ttl']:
                    st.info(f"TTL: {dns_data['AAAA']['ttl']}s")
            else:
                st.warning("⚠️ IPv6 解析失败")

def main():
    st.set_page_config(
        page_title="DNS 双栈解析对比测试工具",
        page_icon="🌐",
        layout="wide"
    )

    st.title("🌐 DNS 双栈解析对比测试工具")
    st.markdown("*聚焦 IPv4/IPv6 双栈解析能力，直观对比阿里云 DNS vs 谷歌 DNS 解析效果*")

    # 输入区域
    st.subheader("🔍 DNS 测试")
    domain = st.text_input(
        "输入要测试的域名:",
        placeholder="例如: www.baidu.com",
        help="输入一个有效的域名进行 DNS 解析测试"
    )

    if st.button("🚀 开始测试", type="primary", use_container_width=True):
        if not domain.strip():
            st.error("请输入有效的域名")
            return

        # 显示进度条
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("正在测试阿里 DNS...")
        progress_bar.progress(33)

        status_text.text("正在测试 Google DNS...")
        progress_bar.progress(66)

        status_text.text("正在分析结果...")
        progress_bar.progress(100)

        # 执行 DNS 基准测试
        benchmark = DNSBenchmark()
        results = benchmark.benchmark_domain(domain.strip())

        # 清除进度条
        progress_bar.empty()
        status_text.empty()

        # 存储结果到 session_state 用于图表展示
        st.session_state.results = results
        st.session_state.domain = domain

        # 展示结果
        display_results(results, domain)

        # 可视化图表
        st.subheader("📈 性能对比图表")
        fig = create_latency_chart(results)
        st.plotly_chart(fig, use_container_width=True)

        # 分析总结
        st.subheader("📋 测试总结")

        # 计算平均性能
        ali_ipv4_time = results['阿里 DNS']['A']['latency_ms']
        ali_ipv6_time = results['阿里 DNS']['AAAA']['latency_ms']
        google_ipv4_time = results['Google DNS']['A']['latency_ms']
        google_ipv6_time = results['Google DNS']['AAAA']['latency_ms']

        # 比较 IPv6 解析能力
        ali_ipv6_success = len(results['阿里 DNS']['AAAA']['records']) > 0
        google_ipv6_success = len(results['Google DNS']['AAAA']['records']) > 0

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**解析成功率对比:**")
            ipv4_success = all(len(results[dns]['A']['records']) > 0 for dns in DNS_SERVERS.keys())
            ipv6_success = all(len(results[dns]['AAAA']['records']) > 0 for dns in DNS_SERVERS.keys())

            st.metric("IPv4 解析成功率", f"{sum(1 for dns in DNS_SERVERS.keys() if len(results[dns]['A']['records']) > 0)}/2")
            st.metric("IPv6 解析成功率", f"{sum(1 for dns in DNS_SERVERS.keys() if len(results[dns]['AAAA']['records']) > 0)}/2")

        with col2:
            st.markdown("**性能对比分析:**")
            if ali_ipv6_success and not google_ipv6_success:
                st.success("✅ 阿里 DNS 支持 IPv6，而 Google DNS 不支持")
            elif ali_ipv6_success and google_ipv6_success:
                if ali_ipv6_time < google_ipv6_time:
                    st.success(f"✅ 阿里 DNS IPv6 解析快 {google_ipv6_time - ali_ipv6_time:.1f}ms")

            # 平均响应时间比较
            ali_avg = (ali_ipv4_time + ali_ipv6_time) / 2
            google_avg = (google_ipv4_time + google_ipv6_time) / 2

            if ali_avg < google_avg:
                st.success(f"✅ 阿里 DNS 平均响应快 {google_avg - ali_avg:.1f}ms")
            elif google_avg < ali_avg:
                st.info(f"ℹ️ Google DNS 平均响应快 {ali_avg - google_avg:.1f}ms")

    # 页脚
    st.markdown("---")
    st.markdown("*支持 IPv4/IPv6 双栈解析 | DNS 性能对比分析工具*")

if __name__ == "__main__":
    main()

import * as d3 from 'd3';
import { JSDOM } from 'jsdom';
import * as contrib from './create-3d-contrib';
import * as pie from './create-pie-language';
import * as radar from './create-radar-contrib';
import * as colors from './create-css-colors';
import * as util from './utils';
import * as type from './type';

const width = 1280;
const height = 850;

const pieHeight = 200 * 1.3;
const pieWidth = pieHeight * 2;

const radarWidth = 400 * 1.3;
const radarHeight = (radarWidth * 3) / 4;
const radarX = width - radarWidth - 40;

export const createSvg = (
    userInfo: type.UserInfo,
    settings: type.Settings,
    isForcedAnimation: boolean,
): string => {
    let svgWidth = width;
    let svgHeight = height;
    let viewBoxY = 0;
    if (settings.type === 'pie_lang_only') {
        svgWidth = pieWidth;
        svgHeight = pieHeight;
    } else if (settings.type === 'radar_contrib_only') {
        svgWidth = radarWidth;
        svgHeight = radarHeight;
    } else {
        // crop the empty band above the calendar that the radar/pie used to fill
        viewBoxY = 110;
        svgHeight = height - viewBoxY;
    }

    const fakeDom = new JSDOM(
        '<!DOCTYPE html><html><body><div class="container"></div></body></html>',
    );
    const container = d3.select(fakeDom.window.document).select('.container');
    const svg = container
        .append('svg')
        .attr('xmlns', 'http://www.w3.org/2000/svg')
        .attr('width', svgWidth)
        .attr('height', svgHeight)
        .attr('viewBox', `0 ${viewBoxY} ${svgWidth} ${svgHeight}`);

    svg.append('style').html(
        [
            '* { font-family: "Ubuntu", "Helvetica", "Arial", sans-serif; }',
            colors.createCssColors(settings),
        ].join('\n'),
    );

    contrib.addDefines(svg, settings);

    // background
    svg.append('rect')
        .attr('x', 0)
        .attr('y', viewBoxY)
        .attr('width', svgWidth)
        .attr('height', svgHeight)
        .attr('class', 'fill-bg');

    if (settings.type === 'pie_lang_only') {
        // pie chart only
        pie.createPieLanguage(
            svg,
            userInfo,
            0,
            0,
            pieWidth,
            pieHeight,
            settings,
            isForcedAnimation,
        );
    } else if (settings.type === 'radar_contrib_only') {
        // radar chart only
        radar.createRadarContrib(
            svg,
            userInfo,
            0,
            0,
            radarWidth,
            radarHeight,
            settings,
            isForcedAnimation,
        );
    } else {
        // 3D-Contrib Calendar only. The radar chart, language pie, star and
        // fork counters and the date period are intentionally omitted so the
        // graphic shows just the 3D commit city and a single commit count.
        contrib.create3DContrib(
            svg,
            userInfo,
            0,
            0,
            width,
            height,
            settings,
            isForcedAnimation,
        );

        const group = svg.append('g');

        const positionXContrib = (width * 3) / 10;
        const positionYContrib = height - 20;

        group
            .append('text')
            .style('font-size', '32px')
            .style('font-weight', 'bold')
            .attr('x', positionXContrib)
            .attr('y', positionYContrib)
            .attr('text-anchor', 'end')
            .text(util.inertThousandSeparator(userInfo.totalContributions))
            .attr('class', 'fill-strong');

        group
            .append('text')
            .style('font-size', '24px')
            .attr('x', positionXContrib + 10)
            .attr('y', positionYContrib)
            .attr('text-anchor', 'start')
            .text('contributions')
            .attr('class', 'fill-fg');
    }
    return container.html();
};
